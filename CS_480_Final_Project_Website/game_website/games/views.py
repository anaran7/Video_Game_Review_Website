from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import wikipedia

currUser = ''
currGame = ''

# Create your views here.
def home(request):
    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)
    #run sql query and set up dctionary to send data into html
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM game_info WHERE game_info.rank<11;")
    context = {'games': []}

    #parse html data
    for i in cursor:
        image = ''
        try:
            wiki = wikipedia.page(i[1], pageid=None, auto_suggest=False)
            image = wiki.images[0]
        except:
            image = 'https://image.shutterstock.com/image-vector/ui-image-placeholder-wireframes-apps-260nw-1037719204.jpg'
        
        #create dictionary for one instance of the games
        dicStruct = {'rank':'', 'name':'','genre':'','ESRB':'', 'image':''}
        dicStruct['rank'] = i[0]
        dicStruct['name'] = i[1]
        dicStruct['genre'] = i[2]
        dicStruct['ESRB'] = i[3]
        dicStruct['image'] = image
        context['games'].append(dicStruct)

        
    return render(request, 'games/home.html', context)


#@csrf_exempt
def login(request):

    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    global currUser
    context = {'response': ''}
    if request.method == 'POST':
        username = "'" + request.POST['inputUser'] + "'"
        password = "'" + request.POST['inputPassword'] + "'"
        sqlQuery = "SELECT * FROM game_users WHERE game_users.username=" + username + " AND " + "game_users.pword=" + password + ";"
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        if cursor.rowcount == 1:
            currUser = username
            return redirect(home)
        else:
            context['response'] = ': User or password invalid'
            return render(request, 'games/login.html', context)

    return render(request, 'games/login.html')


def register(request):

    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    global currUser
    context = {'response': ''}

    #check if the user inputed register information
    if request.method == 'POST':
        username = "'" + request.POST['inputUser'] + "'"
        password = "'" + request.POST['inputPassword'] + "'"
        if(username == "''" or password == "''"):
            context['response'] = ': Missing username or password'
            return render(request, 'games/register.html', context)
            
        sqlQuery = "SELECT * FROM game_users WHERE game_users.username=" + username + ";"
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        if cursor.rowcount == 1:
            context['response'] = ': Username is taken'
            return render(request, 'games/register.html', context)
        else:
            currUser = username
            #insert user into datatbase
            sqlInsert = "Insert INTO game_users VALUES(" + username + ", " + password + ");"
            cursor.execute(sqlInsert)
            return redirect(home)

    return render(request, 'games/register.html')


#show all games user has made a review on
def user(request):

    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    global currUser
    context = {'games': []}

    #check if a user is logged in
    if currUser == '':
        return redirect(login)


    #run sql query and set up dctionary to send data into html
    cursor = connection.cursor()
    sqlQuery = "SELECT * FROM user_reviews, game_info WHERE game_id=game_info.Rank AND username=" + currUser + ";"
    cursor.execute(sqlQuery)
    context = {'games': []}

    #parse html data
    for i in cursor:
        image = ''
        try:
            wiki = wikipedia.page(i[4], pageid=None, auto_suggest=False)
            image = wiki.images[0]
        except:
            image = 'https://image.shutterstock.com/image-vector/ui-image-placeholder-wireframes-apps-260nw-1037719204.jpg'
        
        #create dictionary for one instance of the games
        dicStruct = {'userName':'', 'rank':'', 'reviewScore':'', 'name':'','genre':'','ESRB':'', 'image':''}
        dicStruct['userName'] = i[0]
        dicStruct['rank'] = i[1]
        dicStruct['reviewScore'] = i[2]
        dicStruct['name'] = i[4]
        dicStruct['genre'] = i[5]
        dicStruct['ESRB'] = i[6]
        dicStruct['image'] = image
        context['games'].append(dicStruct)

        
    return render(request, 'games/user.html', context)


#return single game search in a card like for games with a keyword in it// have ability to add raiting
def singleGame(request):

    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    global currUser
    context = {'games': []}

    #check if a user is logged in
    if currUser == '':
        return redirect(login)
    
    if request.method == "GET":
        title = "'" + request.GET['name'] + "'"
        rank = request.GET['rank']
        #get image for game
        image = ''
        try:
            wiki = wikipedia.page(request.GET['name'], pageid=None, auto_suggest=False)
            image = wiki.images[0]
        except:
            image = 'https://image.shutterstock.com/image-vector/ui-image-placeholder-wireframes-apps-260nw-1037719204.jpg'
        
        cursor = connection.cursor()
        rankQuery = "SELECT * FROM score_info WHERE score_info.rank=" + rank + ";"
        cursor.execute(rankQuery)
        for i in cursor:
            dicStruct = {'name':'', 'rank':'', 'criticScore':'', 'userScore':'', 'image':''}
            dicStruct['rank'] = rank
            dicStruct['name'] = request.GET['name']
            dicStruct['criticScore'] = i[1]
            dicStruct['userScore'] = i[2]
            dicStruct['image'] = image
            context['games'].append(dicStruct)
            break

        return render(request, 'games/singleGame.html', context)
         

    if request.method == "POST":
        title = "'" + request.GET['name'] + "'"
        rank = request.GET['rank']
        reviewScore = request.POST['inputReview']


        #run sql query and set up dctionary to send data into html
        sqlQuery = "SELECT * FROM user_reviews WHERE user_reviews.username=" + currUser + " AND " + "user_reviews.game_id=" + rank + ";"
        cursor = connection.cursor()
        cursor.execute(sqlQuery)

        #check if user already has review
        if cursor.rowcount == 1:
            #update review
            sqlUpdate = "Update user_reviews SET review_Score=" + reviewScore + " WHERE username=" + currUser + " AND game_id=" + rank + ";"
            cursor.execute(sqlUpdate)
            return redirect(user)
        else:
            #insert review
            sqlInsert = "Insert INTO user_reviews VALUES(" + currUser + ", " + rank + ", " + reviewScore + ");"
            cursor.execute(sqlInsert)
            return redirect(user)

        

    

    return render(request, 'games/singleGame.html')


#return a list of games max 10 for games with the title in it
def gameSearch(request):
    global currGame

    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    #run sql query and set up dctionary to send data into html
    cursor = connection.cursor()
    #SELECT * FROM game_info,release_info WHERE game_info.Name LIKE '%Minecraft%' AND game_info.Rank=release_info.Rank;
    sqlQuery = "SELECT * FROM game_info,release_info WHERE game_info.Rank=release_info.Rank AND game_info.Name LIKE" + currGame + "LIMIT 0, 20" + ";"
    cursor.execute(sqlQuery)
    context = {'games': []}

    #parse html data
    for i in cursor:
        image = ''
        try:
            wiki = wikipedia.page(i[1], pageid=None, auto_suggest=False)
            image = wiki.images[0]
        except:
            image = 'https://image.shutterstock.com/image-vector/ui-image-placeholder-wireframes-apps-260nw-1037719204.jpg'
        
        #create dictionary for one instance of the games
        dicStruct = {'rank':'', 'name':'','genre':'','ESRB':'', 'Platform':'', 'Publisher':'', 'Developer':'','image':''}
        dicStruct['rank'] = i[0]
        dicStruct['name'] = i[1]
        dicStruct['genre'] = i[2]
        dicStruct['ESRB'] = i[3]
        dicStruct['Platform'] = i[5]
        dicStruct['Publisher'] = i[6]
        dicStruct['Developer'] = i[7]
        dicStruct['image'] = image
        context['games'].append(dicStruct)

    return render(request, 'games/gameSearch.html', context)


#return a chart for esrb raiting distribution
def ESRB(request):

    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    cursor = connection.cursor()
    cursor.execute("SELECT ESRB_Rating FROM games_database.game_info group by ESRB_Rating order by ESRB_Rating;")
    context = {'raiting': [], 'count': []}

    #parse html data
    for i in cursor:
        context['raiting'].append(i[0])
    
    cursor.execute("SELECT COUNT(*) FROM games_database.game_info WHERE ESRB_Rating IS NULL;")
    for i in cursor:
        context['count'].append(i[0])


    for j in range(1,len(context['raiting'])):
        sqlQuery = "SELECT COUNT(*) FROM games_database.game_info WHERE ESRB_Rating='" + context['raiting'][j] + "';"
        cursor.execute(sqlQuery)
        for i in cursor:
            context['count'].append(i[0])

    return render(request, 'games/ESRB.html', context)


#return a chart for publisher distribution
def publisher(request):

    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    cursor = connection.cursor()
    cursor.execute("SELECT Publisher FROM games_database.release_info group by Publisher order by Publisher;")
    context = {'raiting': [], 'count': []}

    #parse html data
    for i in cursor:
        context['raiting'].append(i[0])
    
    #cursor.execute("SELECT COUNT(*) FROM games_database.release_info WHERE Publisher IS NULL;")
    #for i in cursor:
    #    context['count'].append(i[0])


    for j in range(0,len(context['raiting'])):
        sqlQuery = "SELECT COUNT(*) FROM games_database.release_info WHERE Publisher='" + context['raiting'][j] + "';"
        cursor.execute(sqlQuery)
        for i in cursor:
            context['count'].append(i[0])

    return render(request, 'games/publisher.html', context)


#return a chart for releaseYear distribution
def releaseYear(request):

    global currGame
    if request.method == "GET" and request.GET.get('userInput', 'false') != 'false':
        currGame = "'%" + request.GET.get('userInput', 'false') + "%'"
        return redirect(gameSearch)

    cursor = connection.cursor()
    cursor.execute("SELECT Year FROM games_database.release_info group by Year order by Year;")
    context = {'raiting': [], 'count': []}

    #parse html data
    for i in cursor:
        context['raiting'].append(i[0])
    

    for j in range(0,len(context['raiting'])):
        sqlQuery = "SELECT COUNT(*) FROM games_database.release_info WHERE Year=" + str(context['raiting'][j]) + ";"
        cursor.execute(sqlQuery)
        for i in cursor:
            context['count'].append(i[0])

    return render(request, 'games/releaseYear.html', context)