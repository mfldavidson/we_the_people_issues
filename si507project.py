import requests, json, html
from advanced_expiry_caching import *
from si507project_tools import *
from datetime import datetime, timedelta
import plotly
import plotly.graph_objs
import plotly.tools
from plotly import plotly as ply

plotly.tools.set_credentials_file(username='mfldavidson', api_key='qghsxxdhpcX64Jvpn7VS')

# set up the url and the cache object
BASEURL = 'https://api.whitehouse.gov/v1/petitions.json'
CACHE =  Cache('petitions_cache.json')

# routes
@app.route('/')
def index():
    # get the number of petitions in the database
    petitions = Petition.query.all()
    num_petitions = len(petitions)
    # count the number of petitions created in each month
    timeframe = []
    counts = []
    month = datetime(2017,1,1)
    while month < datetime.today():
        timeframe.append(month.strftime("%b %y"))
        counts.append(countPetitions(petitions, start_date = month, end_date = incrementMonth(month)))
        month = incrementMonth(month)
    # create plot
    plot = plotly.graph_objs.Scatter(
        x = timeframe,
        y = counts,
        name = 'Number of Petitions Created',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )

    data = [plot]
    # Edit the layout
    layout = dict(title = 'Petition Creation by Month',
                  xaxis = dict(title = 'Month'),
                  yaxis = dict(title = 'Number of Petitions Created'),
                  )

    fig = dict(data=data, layout=layout)
    graph = ply.plot(fig, filename='petitions-by-month', auto_open=False)
    graph_html = plotly.tools.get_embed(graph)
    return render_template('index.html', num_petitions=num_petitions, graph_html=graph_html)

@app.route('/issues/')
def all_issues():
    issues = Issue.query.all()
    return render_template('issues.html', issues=issues)

@app.route('/issues/<issue_id>/')
def issue(issue_id):
    issue = Issue.query.filter_by(id=issue_id).first()
    petitions = getPetitionsByIssue(issue_id)
    open_petitions, closed_petitions = splitPetitionsBySignable(petitions)
    open_petitions_table = OpenPetitionTable(open_petitions)
    closed_petitions_table = ClosedPetitionTable(closed_petitions)
    return render_template('specific_issue.html', issue=issue, open_petitions=open_petitions, open_petitions_table=open_petitions_table, closed_petitions=closed_petitions, closed_petitions_table=closed_petitions_table)

# run app
if __name__ == '__main__':
    # get the data from the cache file if it exists and is not expired; else, get request the We the People API and cache the response
    data = CACHE.get(BASEURL)
    if not data:
        data = []
        offset = 0
        for num in range(10):
            params = {'limit':1000,'offset':offset}
            resp = requests.get(BASEURL, params).text
            resp_dict = json.loads(resp)
            data = data + resp_dict['results']
            if len(resp_dict['results']) == 1000:
                offset += 1000
            else:
                break
        CACHE.set(BASEURL, data)
    # create the database
    db.create_all()
    # populate the database with data from the cache/API
    for petition in data:
        # check to see if each type already exists; if not, create it
        for petition_type in petition['petition_type']:
            type_exists = PetitionType.query.filter_by(id=petition_type['id']).first()
            if type_exists:
                continue
            else:
                new_type = PetitionType(id=petition_type['id'],name=html.unescape(petition_type['name']))
                session.add(new_type)
                session.commit()
        # check to see if each issue already exists; if not, create it
        for issue in petition['issues']:
            issue_exists = Issue.query.filter_by(id=issue['id']).first()
            if issue_exists:
                continue
            else:
                new_issue = Issue(id=issue['id'],name=html.unescape(issue['name']))
                session.add(new_issue)
                session.commit()
        # check to see if the petition already exists; if not, create it
        petition_exists = Petition.query.filter_by(id=petition['id']).first()
        if petition_exists:
            # for each issue and type, check if the relationship already exists with the petition
            for petition_type in petition['petition_type']:
                rel_exists = session.query(TypePetitionAssociation).filter(TypePetitionAssociation.type_id == petition_type['id'], TypePetitionAssociation.petition_id == petition_exists.id).first()
                if rel_exists:
                    continue
                else:
                    new_rel = TypePetitionAssociation(type_id=petition_type['id'],petition_id=petition_exists.id)
                    session.add(new_rel)
                    session.commit()
            for issue in petition['issues']:
                rel_exists = session.query(IssuePetitionAssociation).filter(IssuePetitionAssociation.issue_id == issue['id'], IssuePetitionAssociation.petition_id == petition_exists.id).first()
                if rel_exists:
                    continue
                else:
                    new_rel = IssuePetitionAssociation(issue_id=issue['id'],petition_id=petition_exists.id)
                    session.add(new_rel)
                    session.commit()
        else:
            deadline = datetime.fromtimestamp(petition['deadline'])
            created = datetime.fromtimestamp(petition['created'])
            if petition['reachedPublic'] == 0:
                reachedpub = False
            else:
                reachedpub = True
            try:
                resp = html.unescape(petition['response'][0])
            except:
                resp = None
            new_petition = Petition(id=petition['id'],title=html.unescape(petition['title']),body=html.unescape(petition['body']),signature_count=petition['signatureCount'],signatures_needed=petition['signaturesNeeded'],url=html.unescape(petition['url']),deadline_date=deadline,status=petition['status'],response=resp,created_date=created,is_signable=petition['isSignable'],reached_public=reachedpub)
            session.add(new_petition)
            session.commit()
            for petition_type in petition['petition_type']:
                new_rel = TypePetitionAssociation(type_id=petition_type['id'],petition_id=new_petition.id)
                session.add(new_rel)
                session.commit()
            for issue in petition['issues']:
                new_rel = IssuePetitionAssociation(issue_id=issue['id'],petition_id=new_petition.id)
                session.add(new_rel)
                session.commit()
    app.run()
