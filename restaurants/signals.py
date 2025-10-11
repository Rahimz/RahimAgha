from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count, Q
from django.contrib.postgres.aggregates import StringAgg

from .models import VoteResponse, Place, ReviewItem, PlaceReviewItemSummary, Vote, PlaceVoteSummary

def update_place_summaries(place: Place):
    """
    A single function to recalculate and update ALL summaries for a given place.
    It first updates the main PlaceVoteSummary, then the detailed item summaries.
    """
    # --- STAGE 1: Update the master PlaceVoteSummary ---

    # Get or create the main summary object for the place.
    vote_summary, created = PlaceVoteSummary.objects.get_or_create(place=place)

    # Calculate the total number of unique votes (reviews) for the place.
    total_unique_votes = Vote.objects.filter(place=place).count()
    
    # Aggregate the average score from ALL applicable responses for this place.
    all_responses = VoteResponse.objects.filter(vote__place=place, is_applicable=True)
    overall_avg_data = all_responses.aggregate(
        avg_score=Avg('score')
    )

    # Update the master summary object
    vote_summary.total_votes = total_unique_votes
    vote_summary.average_score = overall_avg_data['avg_score'] or 0.0
    vote_summary.save()
    
    # --- STAGE 2: Update the detailed PlaceReviewItemSummary objects ---
    
    # Use Django's aggregation to calculate item-specific data in one query.
    summary_data = all_responses.values('review_item__item_type').annotate(
        avg_score=Avg('score'),
        total=Count('pk'),
        notes=StringAgg(
            'extra_notes',
            delimiter=' | ', 
            filter=Q(extra_notes__isnull=False) & ~Q(extra_notes='')
        )
    )

    current_summaries = {item['review_item__item_type']: item for item in summary_data}
    all_item_types = [choice[0] for choice in ReviewItem.ItemTypeChoice.choices]
    
    for item_type in all_item_types:
        data = current_summaries.get(item_type)

        if data:
            # If there is data, update or create the item summary.
            # CRITICAL: We now pass the vote_summary object we retrieved in Stage 1.
            PlaceReviewItemSummary.objects.update_or_create(
                place=place,
                item_type=item_type,
                defaults={
                    'vote_summary': vote_summary,
                    'average_score': data['avg_score'] or 0.0,
                    'total_votes': data['total'] or 0,
                    'concatenated_notes': data['notes'] or ''
                }
            )
        else:
            # If no votes exist for this item_type, delete its summary object.
            PlaceReviewItemSummary.objects.filter(
                place=place,
                item_type=item_type
            ).delete()


@receiver(post_save, sender=VoteResponse)
@receiver(post_delete, sender=VoteResponse)
def on_vote_response_change(sender, instance, **kwargs):
    """
    Trigger the consolidated summary update when a VoteResponse changes.
    """
    place = instance.vote.place
    update_place_summaries(place)
