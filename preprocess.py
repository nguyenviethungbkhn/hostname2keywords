import pandas as pd
import re, ast
from tldextract import extract

def preprocess_df(df):
    df["count"] = df.groupby(["msisdn", "domain_name"])["domain_name"].transform("count")
    temp = df[df["count"] > 10]
    dn = set(temp["domain_name"])
    dn = [x for x in dn if "dn" not in dn]
    dn = [x.replace("content", "") if "content" in x else x for x in dn]
    dn = [x for x in dn if "static" not in x]
    dn = [x.replace("cdn", "") if "cdn" in x else x for x in dn]
    dn = [x for x in dn if "ad" not in x]
    dn = [x for x in dn if not x.isnumeric()]
    dn = [x for x in dn if "content" not in x]
    dn = [x for x in dn if not re.match("\d+\.\d+\.\d+\.\d+", x)]
    dn = [x.replace("apis", "") if x.endswith("apis") else x for x in dn]
    dn = [x for x in dn if len(x) > 1]
    return list(set(dn))

def filter_url(url):
    sub, dm, suf = extract(url)
    return dm

def merge_columns(desc, web_title, desc_lang, web_title_lang):
    if desc_lang in ["en", "vi"]:
        if desc_lang == web_title_lang:
            return desc + ". " + web_title.strip()
    return ""


if __name__=="__main__":
    df = pd.read_csv("super_rich_full_network.tsv", sep="\t", index_col=0)
    dn = preprocess_df(df)
    # df = pd.read_csv("data/merge_crawled_data.csv")
    # df["merged_text"] = df.apply(lambda x: merge_columns(x.description, x.web_title, x.desc_lang, x.web_title_lang), axis=1)
    # df.to_csv("data/merge_crawled_data.csv", index=False)