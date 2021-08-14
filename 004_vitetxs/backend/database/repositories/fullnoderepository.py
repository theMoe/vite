from sqlalchemy.sql.functions import func
from database.models.locationmodel import DBLocation
from sqlalchemy.sql.expression import desc
from database.models.cyclemodel import DBCycle
from typing import List

from sqlalchemy.orm.session import Session

from database.models.node_status_model import NodeStatus
import requests
from fastapi import status


async def get_node_status_from_vite_api(address: str, cycle: int, db: Session) -> List[NodeStatus]:
    url = f'https://stats.vite.net/api/getAlivePeers?address={address}'
    try:
        response = requests.get(url, timeout=10)
        #print(response.json())
        if (response.status_code is not status.HTTP_200_OK):
            print('Vite API is not available')
            raise 'Vite API not available'
        else:
            node_list = response.json()['list']
            node_objects = []
            for node in node_list:
                node_in_cycle = db.query(DBCycle).filter(DBCycle.cycle == cycle).filter(
                    DBCycle.ip == node['ip']).order_by(desc(DBCycle.cycle)).first()
                node_status = NodeStatus(address=node['address'], 
                                        status=node['isAlive'], 
                                        name=node['nodeName'],
                                        ip=node['ip'], 
                                        version=node['version'], 
                                        block_height=node['height'], 
                                        online_ratio=(node_in_cycle.online_ratio * 100) if node_in_cycle is not None else 0)
                node_objects.append(node_status)
            return node_objects

    except:
        raise 'Vite API not available'

async def get_node_geolocations(db: Session):
    last_cycle = db.query(DBCycle).order_by(desc(DBCycle.cycle)).first().cycle
    active_ips = db.query(DBCycle.ip).filter(DBCycle.cycle == last_cycle).all()
    flat_list_active_ips = [item for sublist in active_ips for item in sublist]
    locations_sum = db.query(DBLocation.country, DBLocation.country_code, func.count(DBLocation.ip)).filter(DBLocation.ip.in_(flat_list_active_ips)).group_by(DBLocation.country, DBLocation.country_code).all()
    cities_sum = db.query(DBLocation.city, DBLocation.lat, DBLocation.lon).filter(DBLocation.ip.in_(flat_list_active_ips)).group_by(DBLocation.lat, DBLocation.lon, DBLocation.city).all()
    countries = []
    cities = []
    for each in locations_sum:
        countries.append({'name': each[0], 'id': each[1], 'value': each[2]})
    for each in cities_sum:
        cities.append({'title':each[0] ,'latitude': each[1], 'longitude': each[2]})

    return {'countries': countries, 'cities': cities}

async def get_active_node_count(db: Session):
    last_cycle = db.query(DBCycle).order_by(desc(DBCycle.cycle)).first().cycle
    active_count = db.query(DBCycle.ip).filter(DBCycle.cycle == last_cycle).count()
    return active_count