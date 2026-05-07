def compute_ctr(clicks, impressions):
    return clicks / impressions if impressions > 0 else 0


def compute_cpc(cost, clicks):
    return cost / clicks if clicks > 0 else 0


def calculate_metrics(campaigns):
    total_clicks = 0
    total_impressions = 0
    total_cost = 0

    for campaign in campaigns:
        total_clicks += campaign["clicks"]
        total_impressions += campaign["impressions"]
        total_cost += campaign["cost"]

    ctr = compute_ctr(total_clicks, total_impressions)
    cpc = compute_cpc(total_cost, total_clicks)

    return {
        "total_clicks": total_clicks,
        "total_impressions": total_impressions,
        "total_cost": total_cost,
        "ctr": ctr,
        "cpc": cpc
    }


campaign_data = [
    {"name": "Campaign A", "clicks": 120, "impressions": 3000, "cost": 50},
    {"name": "Campaign B", "clicks": 200, "impressions": 6500, "cost": 80},
    {"name": "Campaign C", "clicks": 90, "impressions": 5000, "cost": 40}
]

results = calculate_metrics(campaign_data)

print("\n=== Overall Metrics ===")
print(results)

print("\n=== Campaign Performance ===")
for campaign in campaign_data:
    ctr = compute_ctr(campaign["clicks"], campaign["impressions"])
    print(f"{campaign['name']} -> CTR: {ctr:.2%}")

best_campaign = max(
    campaign_data,
    key=lambda x: compute_ctr(x["clicks"], x["impressions"])
)

print(f"\nBest Campaign: {best_campaign['name']}")