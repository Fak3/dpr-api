from flask import Blueprint, render_template, json
from flask import current_app as app
from app.mod_site.models import Catalog

mod_site = Blueprint('site', __name__)
catalog = Catalog()

@mod_site.route("/", methods=["GET"])
def home():
    """
    Loads home page
    ---
    tags:
      - site
    responses:
      404:
        description: Publiser does not exist
      200:
        description: Succesfuly loaded home page
    """
    
    return render_template("index.html", title= 'Home'), 200

@mod_site.route("/<owner>/<id>", methods=["GET"])
def datapackage_show(owner, id):
    """
    Loads datapackage page for given owner 
    ---
    tags:
      - site
    parameters:
      - name: owner
        in: path
        type: string
        required: true
        description: datapackage owner name
      - name: id
        in: path
        type: string
        description: datapackage name
    responses:
      404:
        description: Datapackage does not exist
      200:
        description: Succesfuly loaded
    """
    metadata = json.loads(app.test_client().get('/api/{owner}/{id}'.format(owner=owner, id=id)).data)
    if metadata['status'] == 'KO':
        return "404 Not Found", 404
    dataset = metadata['data']
    resources = dataset['resources']
    dataViews = dataset['views'] or []
    
    return render_template("dataset.html", dataset= dataset, showDataApi=True, jsonDataPackage=dataset, dataViews=dataViews), 200