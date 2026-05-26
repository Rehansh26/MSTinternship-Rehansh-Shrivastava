from .models import BusinessCard, Company, Event, KnowledgeEntity, KnowledgeRelationship


def normalize_name(value):
    if not value:
        return ""
    return " ".join(value.lower().strip().split())


def get_or_create_entity(*, entity_type, source_table, source_id, display_name, user=None, verified=True):
    entity, created = KnowledgeEntity.objects.get_or_create(
        entity_type=entity_type,
        source_table=source_table,
        source_id=source_id,
        defaults={
            "display_name": display_name or "Unnamed",
            "canonical_name": normalize_name(display_name or "Unnamed"),
            "is_verified": verified,
            "created_by": user,
        },
    )
    if not created:
        new_name = display_name or entity.display_name
        entity.display_name = new_name
        entity.canonical_name = normalize_name(new_name)
        entity.is_verified = verified
        entity.save(update_fields=["display_name", "canonical_name", "is_verified"])
    return entity


def create_or_update_relationship(
    *, source_entity, relationship_type, target_entity,
    source_type=None, source_id=None, confidence=1.0, weight=1.0, user=None
):
    relationship, created = KnowledgeRelationship.objects.get_or_create(
        source_entity=source_entity,
        relationship_type=relationship_type,
        target_entity=target_entity,
        defaults={
            "source_type": source_type,
            "source_id": source_id,
            "confidence": confidence,
            "weight": weight,
            "created_by": user,
        },
    )
    if not created:
        relationship.confidence = max(relationship.confidence, confidence)
        relationship.weight = max(relationship.weight, weight)
        relationship.save(update_fields=["confidence", "weight"])
    return relationship


def sync_card_to_graph(card, user=None):
    contact_name = f"{card.first_name} {card.last_name or ''}".strip()
    contact_entity = get_or_create_entity(
        entity_type="contact",
        source_table="scanner_businesscard",
        source_id=card.id,
        display_name=contact_name,
        user=user,
    )

    if card.company_link:
        company_entity = get_or_create_entity(
            entity_type="company",
            source_table="scanner_company",
            source_id=card.company_link.id,
            display_name=card.company_link.name,
            user=user,
        )
        create_or_update_relationship(
            source_entity=contact_entity,
            relationship_type="WORKS_AT",
            target_entity=company_entity,
            source_type="approved_contact",
            source_id=card.id,
            user=user,
        )

    if card.met_at_event:
        event_entity = get_or_create_entity(
            entity_type="event",
            source_table="scanner_event",
            source_id=card.met_at_event.id,
            display_name=card.met_at_event.name,
            user=user,
        )
        create_or_update_relationship(
            source_entity=contact_entity,
            relationship_type="MET_AT",
            target_entity=event_entity,
            source_type="approved_contact",
            source_id=card.id,
            user=user,
        )

    for domain in card.domains.all():
        domain_entity = get_or_create_entity(
            entity_type="domain",
            source_table="scanner_domain",
            source_id=domain.id,
            display_name=domain.name,
            user=user,
        )
        create_or_update_relationship(
            source_entity=contact_entity,
            relationship_type="BELONGS_TO_DOMAIN",
            target_entity=domain_entity,
            source_type="domain_tag",
            source_id=domain.id,
            user=user,
        )

    for opp in card.opportunities.all():
        opp_entity = get_or_create_entity(
            entity_type="opportunity",
            source_table="scanner_opportunity",
            source_id=opp.id,
            display_name=opp.title,
            user=user,
        )
        create_or_update_relationship(
            source_entity=contact_entity,
            relationship_type="LINKED_TO_OPPORTUNITY",
            target_entity=opp_entity,
            source_type="opportunity",
            source_id=opp.id,
            user=user,
        )

    return contact_entity


def get_contacts_at_company_via_graph(company_id):
    try:
        company_entity = KnowledgeEntity.objects.get(
            entity_type="company",
            source_table="scanner_company",
            source_id=company_id,
        )
    except KnowledgeEntity.DoesNotExist:
        return BusinessCard.objects.none()

    relationships = KnowledgeRelationship.objects.filter(
        relationship_type="WORKS_AT",
        target_entity=company_entity,
        source_entity__entity_type="contact",
    ).select_related("source_entity")

    contact_ids = [rel.source_entity.source_id for rel in relationships]
    return BusinessCard.objects.filter(id__in=contact_ids, is_approved=True).order_by("-scanned_at")


def get_contacts_by_domain_via_graph(domain_id):
    try:
        domain_entity = KnowledgeEntity.objects.get(
            entity_type="domain",
            source_table="scanner_domain",
            source_id=domain_id,
        )
    except KnowledgeEntity.DoesNotExist:
        return BusinessCard.objects.none()

    relationships = KnowledgeRelationship.objects.filter(
        relationship_type="BELONGS_TO_DOMAIN",
        target_entity=domain_entity,
        source_entity__entity_type="contact",
    ).select_related("source_entity")

    contact_ids = [rel.source_entity.source_id for rel in relationships]
    return BusinessCard.objects.filter(id__in=contact_ids, is_approved=True).order_by("-scanned_at")
