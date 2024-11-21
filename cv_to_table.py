
# %%
import pandas as pd
import tabulate
import yaml
import os, sys
import os.path as path

# %%
CV_OUT = path.join(path.dirname(__file__), "docs", "_data", "cv-fr.yml")

# %%
with open(CV_OUT) as cv_in_f:
    data = yaml.load(cv_in_f, yaml.FullLoader)

# %%
data["teaching"]
# %%
df = pd.DataFrame.from_records(data["teaching"])
df["place"] = df["place"].apply(lambda x: 
                                x["institute"] + ", " +
                                x["university"] + ", " +
                                x["city"] + ", " +
                                x["country"])
df["colaborators"] = df["colaborators"].apply(lambda x: 
                                ", ".join(x) if isinstance(x, list) else x)
df["missions"] = df["missions"].apply(lambda x: 
                                " ; ".join(x) if isinstance(x, list) else x)
df["date"] = df["date"].apply(lambda x:
                                str(x["start"]) + "-" + str(x["end"]) if isinstance(x, dict) else x)
df.iloc[0]
# %%
df = df.sort_values(["place", "date"])
# %%
from IPython.display import display, HTML
column_names = [
    'date', 'place', 'topic',
    'duration', 'kind', 'duration_detail',
    'public', 'colaborators', 'description',
    'missions', 'position']
display(HTML(df.reindex(columns=column_names).fillna('').rename({
    "colaborators": "Collaborateurs",
    "place": "Composante",
    "date": "Année",
    "topic": "Intitulé",
    "duration": "Volume",
    "duration_detail": "Volume détaillé",
    "kind": "Type",
    "public": "Public",
    "description": "Description",
    "missions": "Missions",
    "position": "Statut",
}, axis="columns").style.hide(axis="index").to_html()))
# %%
df.columns
# %%
