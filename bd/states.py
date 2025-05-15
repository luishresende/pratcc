import json
from os import write


def write_states(states):
    with open('states.sql', 'w') as states_sql:
        states_sql.write("INSERT INTO pratcc.state VALUES \n")
        states_sql.write(f"('{states[0]['sigla']}', '{states[0]['nome']}')")
        for state in states[1:]:
            states_sql.write(f", ('{state['sigla']}', '{state['nome']}')")

        states_sql.write(";")


def write_cities(states):
    with open('cities.sql', 'w') as cities_sql:
        cities_sql.write("INSERT INTO pratcc.city VALUES \n")

        for state in states:
            acronym = state['sigla']

            for city in state['cidades']:
                cities_sql.write(f'(NULL, "{acronym}", "{city}"), ')

        cities_sql.write(";")

with open('estados-cidades.json', 'r') as f:
    states = json.loads(f.read())

states = states['estados']

write_cities(states)