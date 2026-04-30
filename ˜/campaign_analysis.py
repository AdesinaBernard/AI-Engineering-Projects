def calculate_metrics(campaigns):
    total_clicks = 0
    total_impressions = 0
    total_cost = 0

    for campaign in campaigns:
        total_clicks += campaign["clicks"]
        total_impressions += campaign["impressions"]
        total_cost += campaign["cost"]
        ctr = total_clicks / total_impressions
        cpc = total_cost / total_clicks

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

#results = calculate_metrics(campaign_data)

#for campaign in campaign_data:
    #campaign_ctr = campaign["clicks"] / campaign["impressions"]
    #print(f"{campaign['name']} -> CTR: {campaign_ctr:.2%}")

best_campaign = max(campaign_data, key=lambda x: x["clicks"] / x["impressions"])
print(f"Best Campaign: {best_campaign['name']}")