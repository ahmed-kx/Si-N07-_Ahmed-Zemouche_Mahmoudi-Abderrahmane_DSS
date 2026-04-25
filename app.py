from pathlib import Path
from xml.dom import minidom
import xml.etree.ElementTree as ET

from flask import Flask, render_template, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
XML_FILE = BASE_DIR / "transport.xml"

app = Flask(__name__, template_folder=str(BASE_DIR), static_folder=None)


def load_station_map():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    station_map = {}
    for station in root.find("stations").findall("station"):
        station_map[station.get("id")] = station.get("name")

    return station_map


def get_trip_price_bounds(trip_element):
    prices = [int(class_node.get("price")) for class_node in trip_element.findall("class")]
    return min(prices), max(prices)


def build_trip_summary(line_element, trip_element, station_map):
    departure_id = line_element.get("departure")
    arrival_id = line_element.get("arrival")
    schedule = trip_element.find("schedule")
    min_price, max_price = get_trip_price_bounds(trip_element)

    classes = []
    for class_node in trip_element.findall("class"):
        classes.append(
            {
                "type": class_node.get("type"),
                "price": int(class_node.get("price")),
            }
        )

    return {
        "line_code": line_element.get("code"),
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "departure_city": station_map.get(departure_id, departure_id),
        "arrival_city": station_map.get(arrival_id, arrival_id),
        "trip_code": trip_element.get("code"),
        "trip_type": trip_element.get("type"),
        "departure_time": schedule.get("departure"),
        "arrival_time": schedule.get("arrival"),
        "days": trip_element.findtext("days", default=""),
        "classes": classes,
        "min_price": min_price,
        "max_price": max_price,
    }


def filter_trips(departure="", arrival="", train_type="", max_price=""):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    station_map = load_station_map()

    departure = departure.strip().lower()
    arrival = arrival.strip().lower()
    train_type = train_type.strip().lower()
    max_price_value = int(max_price) if max_price else None

    results = []

    for line in root.find("lines").findall("line"):
        trip_nodes = line.find("trips").findall("trip")

        for trip in trip_nodes:
            trip_info = build_trip_summary(line, trip, station_map)

            if departure and trip_info["departure_city"].lower() != departure:
                continue

            if arrival and trip_info["arrival_city"].lower() != arrival:
                continue

            if train_type and trip_info["trip_type"].lower() != train_type:
                continue

            if max_price_value is not None and trip_info["min_price"] > max_price_value:
                continue

            results.append(trip_info)

    return results


def dom_text_from_first_tag(parent, tag_name):
    nodes = parent.getElementsByTagName(tag_name)
    if not nodes:
        return ""

    if not nodes[0].firstChild:
        return ""

    return nodes[0].firstChild.nodeValue.strip()


def find_trip_by_code_with_dom(trip_code):
    if not trip_code:
        return None

    document = minidom.parse(str(XML_FILE))
    line_nodes = document.getElementsByTagName("line")

    station_map = {}
    for station in document.getElementsByTagName("station"):
        station_map[station.getAttribute("id")] = station.getAttribute("name")

    for line in line_nodes:
        trip_nodes = line.getElementsByTagName("trip")

        for trip in trip_nodes:
            if trip.getAttribute("code").lower() != trip_code.lower().strip():
                continue

            schedule_nodes = trip.getElementsByTagName("schedule")
            schedule = schedule_nodes[0] if schedule_nodes else None

            classes = []
            prices = []
            for class_node in trip.getElementsByTagName("class"):
                price = int(class_node.getAttribute("price"))
                prices.append(price)
                classes.append(
                    {
                        "type": class_node.getAttribute("type"),
                        "price": price,
                    }
                )

            departure_id = line.getAttribute("departure")
            arrival_id = line.getAttribute("arrival")

            return {
                "line_code": line.getAttribute("code"),
                "departure_id": departure_id,
                "arrival_id": arrival_id,
                "departure_city": station_map.get(departure_id, departure_id),
                "arrival_city": station_map.get(arrival_id, arrival_id),
                "trip_code": trip.getAttribute("code"),
                "trip_type": trip.getAttribute("type"),
                "departure_time": schedule.getAttribute("departure") if schedule else "",
                "arrival_time": schedule.getAttribute("arrival") if schedule else "",
                "days": dom_text_from_first_tag(trip, "days"),
                "classes": classes,
                "min_price": min(prices) if prices else 0,
                "max_price": max(prices) if prices else 0,
            }

    return None


def calculate_statistics_with_elementtree():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    station_map = load_station_map()

    line_statistics = []
    trip_type_counts = {}

    for line in root.find("lines").findall("line"):
        trip_summaries = []

        for trip in line.find("trips").findall("trip"):
            summary = build_trip_summary(line, trip, station_map)
            trip_summaries.append(summary)

            trip_type = summary["trip_type"]
            trip_type_counts[trip_type] = trip_type_counts.get(trip_type, 0) + 1

        if trip_summaries:
            cheapest_trip = min(trip_summaries, key=lambda item: item["min_price"])
            most_expensive_trip = max(trip_summaries, key=lambda item: item["max_price"])

            line_statistics.append(
                {
                    "line_code": line.get("code"),
                    "departure_city": station_map.get(line.get("departure"), line.get("departure")),
                    "arrival_city": station_map.get(line.get("arrival"), line.get("arrival")),
                    "cheapest_trip": cheapest_trip,
                    "most_expensive_trip": most_expensive_trip,
                }
            )

    return line_statistics, dict(sorted(trip_type_counts.items()))


@app.route("/", methods=["GET"])
def index():
    stations = load_station_map()
    station_names = sorted(stations.values())
    train_types = sorted(
        {
            trip["trip_type"]
            for trip in filter_trips()
        }
    )

    trip_code = request.args.get("trip_code", "").strip()
    departure = request.args.get("departure", "").strip()
    arrival = request.args.get("arrival", "").strip()
    train_type = request.args.get("train_type", "").strip()
    max_price = request.args.get("max_price", "").strip()

    searched_trip = find_trip_by_code_with_dom(trip_code) if trip_code else None
    filtered_trips = filter_trips(
        departure=departure,
        arrival=arrival,
        train_type=train_type,
        max_price=max_price,
    )
    line_statistics, trip_type_counts = calculate_statistics_with_elementtree()

    return render_template(
        "index.html",
        filters={
            "trip_code": trip_code,
            "departure": departure,
            "arrival": arrival,
            "train_type": train_type,
            "max_price": max_price,
        },
        searched_trip=searched_trip,
        filtered_trips=filtered_trips,
        line_statistics=line_statistics,
        trip_type_counts=trip_type_counts,
        station_names=station_names,
        train_types=train_types,
    )


@app.route("/style.css")
def style_file():
    return send_from_directory(BASE_DIR, "style.css", mimetype="text/css")


@app.route("/transport.xml")
def xml_file():
    return send_from_directory(BASE_DIR, "transport.xml", mimetype="application/xml")


@app.route("/trains.xsl")
def xsl_file():
    return send_from_directory(BASE_DIR, "trains.xsl", mimetype="application/xml")


if __name__ == "__main__":
    app.run(debug=True)
