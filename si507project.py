import requests, json, html
from advanced_expiry_caching import *
from si507project_tools import *
from datetime import datetime, timedelta
import plotly
import plotly.graph_objs
import plotly.tools
from plotly import plotly as ply

# plotly.tools.set_credentials_file(username='mfldavidson', api_key='ENTER_API_KEY_HERE')

# set up the url and the cache object
BASEURL = 'https://api.whitehouse.gov/v1/petitions.json'
CACHE =  Cache('petitions_cache.json')

# routes
@app.route('/')
def index():
    # get the number of petitions in the database
    petitions = Petition.query.all()
    num_petitions = len(petitions)
    petitions.sort(key=lambda petition: petition.signature_count, reverse=True)
    most_sigs = petitions[0]
    diff = most_sigs.signature_count - petitions[1].signature_count
    # get the petitions that are pending response over 90 days
    ninety_days_ago = datetime.today() - timedelta(days=90)
    petitions_without_response = Petition.query.filter(Petition.status=='pending response', Petition.deadline_date < ninety_days_ago)
    # create tables with the petitions
    pending_petitions_table = ClosedPetitionTable(petitions_without_response)
    return render_template('index.html', num_petitions=num_petitions, most_sigs=most_sigs, diff=diff, pending_petitions_table=pending_petitions_table)

@app.route('/viz/')
def charts():
    # all_petitions_graph_html = plotly.tools.get_embed(all_petitions_graph)
    # petitions_by_issue_graph_html = plotly.tools.get_embed(petitions_by_issue_graph)
    return render_template('viz.html', omitted=omitted)

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
            # if the data returned in the last API request was less than 1000 petitions, this means there are no more petitions--check if it is 1000 and if so, request again, if not, move on
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
            new_petition = Petition(id=petition['id'],title=html.unescape(petition['title']),body=html.unescape(petition['body']),signature_count=petition['signatureCount'],signatures_needed=petition['signaturesNeeded'],url=html.unescape(petition['url']),deadline_date=deadline,status=petition['status'],created_date=created,is_signable=petition['isSignable'],reached_public=reachedpub)
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
##### The following code was used to create the visualizations as online plots in my Plotly account. It has been commented out because in order for you to run this code when you are grading, you would have to create a Plotly credentials file on your own computer with my credentials, which is not ideal for any of us. Per Piazza post @209, I kept this code but commented out the parts that require Plotly so you can see it, and simply embedded the plots in iframes.
    ### create the graph ###
    # create the timeframe (month/year) list and the line for all petitions, regardless of issue, and create a line
    petitions = Petition.query.all()
    timeframe = []
    counts = []
    month = datetime(2017,1,1)
    while month < datetime.today():
        timeframe.append(month.strftime("%b %y"))
        counts.append(countPetitions(petitions, start_date = month, end_date = incrementMonth(month)))
        month = incrementMonth(month)
    # plot = plotly.graph_objs.Scatter(
    #     x = timeframe,
    #     y = counts,
    #     name = 'All Petitions',
    #     line = dict(
    #         color = ('rgb(11,66,60)'),
    #         width = 4))
    # data = [plot]
    # # add layout settings and create the graph
    # layout = dict(title = 'Petition Creation by Month - All Petitions',
    #               xaxis = dict(title = 'Month'),
    #               yaxis = dict(title = 'Number of Petitions Created'),
    #               )
    # fig = dict(data=data, layout=layout)
    # all_petitions_graph = ply.plot(fig, filename='all-petitions-by-month', auto_open=False)

    # create the lines for each individual issue's petitions
    # colors = ['rgb(139,0,0)','rgb(255,140,0)','rgb(255,215,0)','rgb(46,139,87)','rgb(70,130,180)','rgb(65,105,225)','rgb(72,61,139)','rgb(186,85,211)','rgb(255,99,71)','rgb(107,142,35)','rgb(144,238,144)','rgb(11,66,60)','rgb(11,66,60)','rgb(95,158,160)','rgb(25,25,112)']# list of colors to use for the lines
    # data = [] # empty list to add all of the plots to
    omitted = {}
    # color_index = 0
    issues = Issue.query.all()
    for issue in issues:
        petitions = getPetitionsByIssue(issue.id)
        if len(petitions) > 100:
            continue
            # counts = []
            # month = datetime(2017,1,1)
            # while month < datetime.today():
            #     counts.append(countPetitions(petitions, start_date = month, end_date = incrementMonth(month)))
            #     month = incrementMonth(month)
            # plot = plotly.graph_objs.Scatter(
            #     x = timeframe,
            #     y = counts,
            #     name = '{} Petitions'.format(issue.name),
            #     line = dict(
            #         color = (colors[color_index]),
            #         width = 4))
            # color_index += 1
            # data.append(plot)
        else:
            omitted[issue.name] = petitions
    # add layout settings and create the graph
    # layout = dict(title = 'Petition Creation by Month Separated By Issue Tag for Issues with Over 100 Total Petitions, All Time',
    #               xaxis = dict(title = 'Month'),
    #               yaxis = dict(title = 'Number of Petitions Created'),
    #               )
    # fig = dict(data=data, layout=layout)
    # petitions_by_issue_graph = ply.plot(fig, filename='petitions-by-issue-by-month', auto_open=False)

    # run the app
    app.run()
