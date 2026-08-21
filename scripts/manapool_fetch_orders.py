#!/usr/bin/env python3
"""
Fetch all order details from Mana Pool given a session cookie or API token.
Usage:
    python3 scripts/manapool_fetch_orders.py --cookie "<mp-auth-token-value>"
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error

ORDER_IDS = [
    "7e321871-6703-45da-8c53-5244c5df4113",
    "dd092040-53d3-416a-b9d5-50e529dd8881",
    "55098430-ecf6-4960-9ac4-0b8aa120f9bb",
    "607a3ffd-93bf-4faf-87eb-2937f825a982",
    "3edf0a24-594c-47b3-a3dd-72744a9551d6",
    "4bdf8250-f88e-4ce8-ae4c-8ad6b5ee5969",
    "70f9d81c-6a66-4495-a491-226f988632ce",
    "4d69d549-c2df-4b9e-9ebd-d45ea870fa26",
    "6dc1d469-2451-42f5-917a-f21f6c8e9297",
    "49b4cc45-c63b-4dec-a020-ae99439b3e7b",
    "2d400e4d-726f-4244-94dd-f17898323a5a",
    "61c6817b-cc26-43a7-8e35-6c20367f9035",
    "ee7b429f-ea73-4b29-a9dc-b9ba20230d34",
    "3229bcec-cc69-47b5-9f63-a6d2e70be562",
    "cdd9b958-25ca-46b2-92b7-2b673326e582",
    "0e0f6691-b94e-45ce-a7a5-eaca6fe5ae77",
    "64dce07e-cd25-49af-9d65-1a40624fa16b",
    "24b34500-701a-4906-a0fe-666dd93a3c02",
    "d4582a2f-14e9-4944-a634-4a63b7c18fa4",
    "e71eed30-3590-46f5-8b53-ba610be06ae6",
    "52699525-10e7-449c-b2a8-fca9d64bc8dc",
    "52b3e7f0-b6b6-4b3f-a7b4-cc6c9f99e264",
    "143c9bca-5ac2-450a-91f8-85dc4ebc66ea",
    "fe7903c7-b88a-4de0-bbcc-fc011c3377f6"
]

def fetch_order(order_id, headers):
    url = f"https://manapool.com/api/v1/buyer/orders/{order_id}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching order {order_id}: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch and analyze all Mana Pool order items.")
    parser.add_argument("--cookie", help="mp-auth-token cookie value")
    parser.add_argument("--token", help="Mana Pool access token (mpat_...)")
    parser.add_argument("--email", help="Mana Pool account email")
    parser.add_argument("--output", default=os.path.join("cache", "all_purchased_items.json"), help="Output JSON path")
    args = parser.parse_args()

    headers = {"Accept": "application/json", "User-Agent": "MTGDeckCollection/1.0"}
    if args.cookie:
        headers["Cookie"] = f"mp-auth-token={args.cookie}"
    elif args.token and args.email:
        headers["X-ManaPool-Access-Token"] = args.token
        headers["X-ManaPool-Email"] = args.email
    else:
        print("Please provide --cookie '<value>' or --token '<token>' --email '<email>'")
        sys.exit(1)

    all_items = []
    print(f"Fetching details for {len(ORDER_IDS)} orders...")
    for idx, oid in enumerate(ORDER_IDS, 1):
        print(f"  [{idx:>2}/{len(ORDER_IDS)}] Fetching order {oid[:8]}...", end="\r", flush=True)
        data = fetch_order(oid, headers)
        if not data:
            continue
        order = data.get("order", data)
        created_at = order.get("created_at", "")[:10]
        order_num = order.get("order_number", "")
        
        # Parse nested seller items
        seller_details = order.get("order_seller_details", [])
        if seller_details:
            for seller in seller_details:
                seller_name = seller.get("seller_username", "Unknown Seller")
                for item in seller.get("items", []):
                    single = item.get("product", {}).get("single") or item.get("single") or {}
                    card_name = single.get("name") or item.get("product", {}).get("sealed", {}).get("name", "Unknown Item")
                    set_code = (single.get("set") or single.get("set_code", "")).upper()
                    condition = single.get("condition_id", "")
                    finish = single.get("finish_id", "")
                    price_dollars = (item.get("price_cents") or 0) / 100.0
                    qty = item.get("quantity", 1)
                    all_items.append({
                        "name": card_name,
                        "set": set_code,
                        "condition": condition,
                        "finish": finish,
                        "price": price_dollars,
                        "quantity": qty,
                        "order_number": order_num,
                        "seller": seller_name,
                        "date": created_at
                    })
        elif "items" in order:
            for item in order.get("items", []):
                single = item.get("single", {})
                card = single.get("card", {})
                card_name = card.get("name", item.get("description", "Unknown"))
                set_code = card.get("set_code", "").upper()
                seller = item.get("seller", {})
                seller_name = seller.get("name", "Unknown Seller")
                condition = single.get("condition_id", "")
                finish = single.get("finish_id", "")
                price_dollars = (item.get("price_cents") or 0) / 100.0
                qty = item.get("quantity", 1)
                all_items.append({
                    "name": card_name,
                    "set": set_code,
                    "condition": condition,
                    "finish": finish,
                    "price": price_dollars,
                    "quantity": qty,
                    "order_number": order_num,
                    "seller": seller_name,
                    "date": created_at
                })
        time.sleep(0.2)

    all_items.sort(key=lambda x: x["price"], reverse=True)
    
    # Save full JSON cache of purchases
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2)
    print(f"\nSaved {len(all_items)} purchased items to {args.output}")

    print("\n" + "=" * 85)
    print(f"{'MOST EXPENSIVE CARDS PURCHASED':^85}")
    print("=" * 85)
    for i, it in enumerate(all_items[:50], 1):
        cond_str = f"[{it['condition']}{' Foil' if it['finish'] == 'FO' else ''}]"
        print(f"{i:>2}. ${it['price']:>7.2f} | {it['name']:<35} ({it['set']:<4}) {cond_str:<11} | {it['date']} (Order #{it['order_number']})")

if __name__ == "__main__":
    main()
