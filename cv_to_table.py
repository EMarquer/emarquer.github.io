
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
df["diploma"] = df["place"].apply(lambda x: 
                                x["institute"].split(", ", 1)[-1]
                                )
df["place"] = df["place"].apply(lambda x: 
                                x["institute"] + ", "
                                + x["university"] + ", "
                                + x["city"] + ", "
                                #+ x["country"]
                                )
df["colaborators"] = df["colaborators"].apply(lambda x: 
                                ", ".join(x) if isinstance(x, list) else x)
df["lang"] = df["lang"].apply(lambda x: 
                                " et ".join(sorted(x)) if isinstance(x, list) else x)
df["missions"] = df["missions"].apply(lambda x: 
                                " \par ".join(x) if isinstance(x, list) else x)
df["date"] = df["date"].apply(lambda x:
                                str(x["start"]) + "-" + str(x["end"]) if isinstance(x, dict) else x)
df.iloc[0]
# %%
df = df.sort_values(["date", "place", 'topic'], ascending=False)
# %%
from IPython.display import display, HTML
column_names = [
    'status', 'position', 'date', 'place', 'topic',
    'duration', 'kind', 'duration_detail',
    'public', "diploma", "public_mld", 'colaborators', 'description',
    'missions']

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
renaming_cols = {
    "colaborators": "Collaborateurs",
    "place": "Composante",
    "date": "Année",
    "topic": "Intitulé",
    "duration": "Volume HETD",
    "duration_detail": "Volume détaillé",
    "kind": "Nature",
    "diploma": "Diplome",
    "public_mld": "Niveau",
    "description": "Description",
    "missions": "Responsabilités",
    "status": "Statut",
}
df["status"] = df["status"].str.capitalize()
df_ = df.reindex(columns=column_names).fillna('').rename(renaming_cols, axis="columns").replace(
    '&', '\\&', regex=True
)
df_["Année"] = df_["Année"].replace({r"20(\d\d)": r'\1'}, regex=True)
df_["Statut"] = df_["Statut"].replace("Vacataire", "V.")
# df_["Description"] = (df_["Description"] + 
#                       #df_["Missions"].apply(lambda x: " \\par <b>Missions:</b> " + x if x else "") +
#                       df_["Collaborateurs"].apply(lambda x: " \\par <b>Collaborateurs:</b> " + x if x else ""))
# df_["Volume"] = (df_["Volume"] + 
#     df_["Type"].apply(lambda x: " de " + x if x else "") + 
#     df_["Volume détaillé"].apply(lambda x: " (" + x + ")" if x else ""))
df_ = df_.replace(
    {r'<i>(.+?)</i>': r'\\textit{\1}', r'<b>(.+?)</b>': r'\\textbf{\1}'}, regex=True)
print((df_.style.hide(axis="index").hide(axis="columns", subset=["public", "position", "Volume détaillé", "Collaborateurs", "Description"]).to_latex()))
#display(HTML(df_.style.hide(axis="index").hide(axis="columns", subset=["Type", "Volume détaillé", "Collaborateurs"]).to_html()))
# %%
