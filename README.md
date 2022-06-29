# CoinSpace

## Note of Intent

*Ce projet est issu du parcours [Développeur d’application - Python](https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python)
d’[OpenClassrooms](https://openclassrooms.com/).*

Avec l’émergence de la blockchain dans notre quotidien, de plus en plus de projets et d’applications voient le jour, et il peut être parfois difficile de suivre l’état de son portfolio de manière globale.
Chaque blockchain essaie de proposer à ses utilisateurs des avantages par rapport à d’autres (frais de transactions moins élevés, transactions plus rapides, etc.), ce qui fait que parfois, nous nous retrouvons avec 10 ou 20 portefeuilles différents.

**CoinSpace** est là pour y remédier ! Cette application s’adresse à toute personne souhaitant faciliter la gestion de son portfolio crypto.
Il s’agit d’une application permettant de tracker ses actifs sur la blockchain. Vous pourrez entre autres afficher :
- Vos transactions
- Vos actifs
- Perte/gain sur 24 heures
- Solde
- Valeur ($)

Les portefeuilles supportés doivent être sur la blockchain Ethereum / Polygon / Avalanche. La prochaine étape est de rajouter la compatibilité pour les portefeuilles se trouvant sur des plateformes d’échange.

## Installation

This project currently supports PostgreSQL.
Installation: [PostgreSQL](https://www.postgresql.org/download/).

Create a virtual environment with the [venv](https://docs.python.org/3/tutorial/venv.html) module to install the application:
```bash
python -m venv .venv
```

Then, activate the virtual environment:
```bash
.venv/scripts/activate
```

Install the dependencies using the package manager [pip](https://pip.pypa.io/en/stable/):
```bash
pip install -r requirements.txt
```

Finally, create a `.env` file at the project root, and insert the following:
```bash
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY=[RANDOM_KEY]
COINMARKETCAP_API_KEY=[YOUR_CMC_API_KEY]
ETHERSCAN_API_KEY=[YOUR_ETHERSCAN_API_KEY]
POLYGONSCAN_API_KEY=[YOUR_POLYGONSCAN_API_KEY]
SNOWTRACE_API_KEY=[YOUR_SNOWTRACE_API_KEY]
DB_USER=[YOUR_POSTGRE_USER]
DB_PWD=[YOUR_POSTGRE_PASSWORD]
```

Replace values between brackets with your own (don't forget to also remove the brackets).

## Usage

### Creating database

Start PostgreSQL Shell and create a new database named `coinspace`.

```sql
CREATE DATABASE coinspace;
```

### Launching application

Activate the virtual environment and populate the database using:
```bash
python manage.py migrate
```

Then start the application by running the following command:
```bash
python manage.py runserver
```

### Running tests

This project uses [pytest](https://docs.pytest.org/en/6.2.x/) instead of default Django [unittest](https://docs.djangoproject.com/fr/4.0/topics/testing/overview/).

To start tests, simply run:
```bash
pytest tests/unit
```