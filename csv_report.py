import csv

def write_csv_report(page_data, filename="report.csv"):
    
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["page_url", "h1", "first_paragraph", "outgoing_link_urls", "image_urls"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in page_data.values():
            writer.writerow({
                "page_url": item["url"], 
                "h1": item["h1"], 
                "first_paragraph": item["first_paragraph"], 
                "outgoing_link_urls": ";".join(item["outgoing_links"]), 
                "image_urls": ";".join(item["image_urls"])
            })
        
