import geojson
import overpy
import os
import pandas as pd

api = overpy.Overpass()

# Function to query Overpass API based on organization type and location
def query_organization(organization_type, min_lat, min_lon, max_lat, max_lon):
    query = f"""
    way({min_lat}, {min_lon}, {max_lat}, {max_lon})["amenity" = "{organization_type}"];
    (._;>;);
    out body;
    """
    result = api.query(query)
    return result

# Example usage with organization type and location coordinates
organization_type = input("Enter the type of organization (e.g., school, hospital, restaurant): ").strip()
min_lat, min_lon = 41.2683, 1.9633
max_lat, max_lon = 41.4522, 2.1976

result = query_organization(organization_type, min_lat, min_lon, max_lat, max_lon)

# Collect the details of the organizations
data = []
for way in result.ways:
    data.append({
        "Name": way.tags.get("name", "n/a"),
        "Postnummer": way.tags.get("addr:postcode", "n/a"),
        "Kategorie": way.tags.get("amenity", "n/a"),
        "Strasse": way.tags.get("addr:street", "n/a"),
        "Hausnummer": way.tags.get("addr:housenumber", "n/a"),
        "Website": way.tags.get("website", "n/a"),
        "Telefonnummer": way.tags.get("phone", "n/a"),
        "Operator": way.tags.get("operator", "n/a"),
        "Quelle fuer Energie": way.tags.get("generator:source", "n/a"),
        "Energieverbrauch": way.tags.get("generator:output:electricity", "n/a"),
        #"Nodes": ", ".join([str(node.id) for node in way.nodes])  # Uncomment if you need nodes
    })

# Create a DataFrame and save it to an Excel file
df = pd.DataFrame(data)
output_file = f"{organization_type}_organizations.xlsx"
df.to_excel(output_file, index=False)

print(f"Data saved to {output_file}")

# Example test function
def test_overpass_unknown_http_status_code():
    e = overpy.exception.OverpassUnknownHTTPStatusCode(123)
    assert e.code == 123
    assert str(e).endswith("123")

# Run the test
test_overpass_unknown_http_status_code()