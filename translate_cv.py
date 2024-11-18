# %%
# !pip install --proxy="http://cache-adm:8080" "niquests>=3.10,<4" 
# %%
# %env HTTP_PROXY="http://cache-adm:8080"
# %env HTTPS_PROXY="http://cache-adm:8080"
# %env ALL_PROXY="socks5://cache-adm:8080"
# %%
from typing import Literal
import yaml
import os, sys
import os.path as path

# %%
CV_IN = path.join(path.dirname(__file__), "docs", "_data", "cv.yml")
CV_OUT = path.join(path.dirname(__file__), "docs", "_data", "cv-fr.yml")

# %%
with open(CV_IN) as cv_in_f:
    data = yaml.load(cv_in_f, yaml.FullLoader)

# %%
import translators as ts
# ### usage
#_ = ts.preaccelerate_and_speedtest()  # Optional. Caching sessions in advance, which can help improve access speed.
TRANSLATORS = ["google"]#, "deepl"]
for tl_engine in TRANSLATORS:
    print(
        ts.translate_text(
            query_text="this is a test",
            translator=tl_engine,
            from_language="en",
            to_language="fr"
            ))

# %%
def deep_translate(nested_dict_or_list_or_str, tl_engine="google", from_language="en", to_language="fr", untranslatable: Literal["ignore", "raise"] = "ignore"):
    if isinstance(nested_dict_or_list_or_str, str):
        return ts.translate_text(
            query_text=nested_dict_or_list_or_str,
            translator=tl_engine,
            from_language=from_language,
            to_language=to_language,
            if_use_preacceleration=True
            )
    elif isinstance(nested_dict_or_list_or_str, list):
        return [deep_translate(v) for v in nested_dict_or_list_or_str]
    elif isinstance(nested_dict_or_list_or_str, dict):
        return {k: deep_translate(v) for k, v in nested_dict_or_list_or_str.items()}
    else:
        if untranslatable=="raise":
            raise TypeError(f"got {type(nested_dict_or_list_or_str)}, but input must be str, list, dict, or a nested combination of them")
        else:
            return nested_dict_or_list_or_str

# %%
DATE_COMPACT = {
    "Janvier":      "Jan.",
    "Février":      "Fév.",
    "Mars":         "Mars",
    "Avril":        "Avr.",
    "Mai":          "Mai",
    "Juin":         "Juin",
    "Juillet":      "Juil.",
    "Août":         "Août.",
    "Septembre":    "Sept.",
    "Octobre":      "Oct.",
    "Novembre":     "Nov.",
    "Décembre":     "Déc.",
}
DATE_COMPACT.update({ # other fixes
    "apprentissage en profondeur": "apprentissage profond",
    "réseaux conceptuels": "treillis de concepts",
    "réseau conceptuel": "treillis de concepts",
    "réseau concept": "treillis de concepts",
    "Stage de fin de recherche en fin de maîtrise": "Stage de recherche de fin de master",
    "Master 1 stage de recherche facultatif": "Stage de recherche facultatif de master 1",
    "Stage de recherche de fin de célibataire": "Stage de recherche de fin de licence",
    "doctorat Étudiant": "Doctorant",
})
def deep_redate(nested_dict_or_list_or_str):
    if isinstance(nested_dict_or_list_or_str, str):
        result = nested_dict_or_list_or_str
        for k, v in DATE_COMPACT.items():
            result = result.replace(k, v)
        return result
    elif isinstance(nested_dict_or_list_or_str, list):
        return [deep_redate(v) for v in nested_dict_or_list_or_str]
    elif isinstance(nested_dict_or_list_or_str, dict):
        return {k: deep_redate(v) for k, v in nested_dict_or_list_or_str.items()}
    else:
        return nested_dict_or_list_or_str


# %%
from pprint import pprint
result = deep_translate(data)
pprint(result)

import pickle
with open("safety.pkl", 'wb') as safety_f:
    pickle.dump(result, safety_f)

# %%
import pickle
with open("safety.pkl", 'rb') as safety_f:
    result = pickle.load(safety_f)
os.makedirs(path.dirname(CV_OUT),exist_ok=True)
with open(CV_OUT, 'w') as cv_out_f:
    data = yaml.dump(
        deep_redate(result), 
        cv_out_f, 
        yaml.SafeDumper, 
        allow_unicode=True)

# %%
