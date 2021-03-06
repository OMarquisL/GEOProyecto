import webapp2
import jinja2
import os

import datetime

import time
import logging
from time import sleep

jinja_current_dir = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)



EDUCATION_NAV = [
    # Button id      link path           display name
    ("Daycare",  "DaycareandPreschool", "Daycare and Preschool"),
    ("Secondary", "SecondarySchool ", "Secondary School"),
    ("Colleges", "CollegesandUniversities", "Colleges and Universities"),
    ("International", "InternationalandBoarding", "International and Boarding Schools"),
    ("Resources", "LearningResources", "Learning Resources")
]

IMMIGRATION_NAV = [

    ("Legal", "LegalResources", "Legal Resources"),
    ("Citizenship", "CitizenshipInfo", "Citizenship Information" ),
    ("Visa", "VisaInfo", "Visa Information"),
    ("StateInfo", "StateInfo", "State Specific Information"),

]

USLIFE_NAV = [
    ("InsuRance", "InsuranceP", "Insurance"),
    ("HouseInfo", "HousingP", "Housing"),
    ("HealthCare", "HealthC", "Healthcare Information"),
    ("BankFin", "BankFinan", "Bank and Financial Information"),
    ("Employmnt", "Employ", "Employment")
]

USCULTURE_NAV = [
    ("SlanG", "SlangP", "Slang"),
    ("PolChan", "PolCliP", "Political Climate"),
    ("SportS", "SportsP", "Sports"),
    ("HoliHist", "HolHisP", "Holidays and Historic Figures"),
    ("StateAt", "StateAttrP", "State Attractions"),
    ("GenTip", "GenTips", "General Tips")
]


from google.appengine.api import users
from google.appengine.ext import ndb

class CssiUser(ndb.Model):

    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    saved_info = ndb.StringProperty()
#   user_name = ndb.StringProperty()
#   last_activity = ndb.DateTimeProperty()

class Question(ndb.Model):
    # askerinfo = ndb.KeyProperty(CssiUser)
    timeasked = ndb.DateTimeProperty()
    # replies = ndb.KeyProperty(Reply, repeated=True)
    question = ndb.StringProperty()
    title = ndb.StringProperty()

class Reply(ndb.Model):
    timegiven = ndb.DateTimeProperty()
    # giverinfo = ndb.KeyProperty(CssiUser)
    reply = ndb.StringProperty()
    # question = ndb.KeyProperty(Question)

class ForumPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/forum.html")
        self.response.write(page_content.render())

class FormSubmit(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/formsubmit.html")
        self.response.write(page_content.render())
    def get(self):
        print "Made it this far"
        #user_name = self.request.get("user_name")
        #user = CssiUser.query(CssiUser.user_name == user_name)
        question = Question(timeasked = datetime.datetime.now(), question = self.request.get("question"), title = self.request.get("title"))
        question.put()
        print "Saved question."
        self.redirect("/questions")
        # self.response.out.write("Yo I saved your question you're welcome")


class ShowQuestions(webapp2.RequestHandler):
    def get(self):
        params = {}
        params['questions'] = []
        for question in Question.query().fetch():
            params['questions'].append(question)
        content = jinja_current_dir.get_template("Templates/questions.html")
        self.response.write(content.render(params))




jinja_current_dir = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

class MainHandler(webapp2.RequestHandler):
  def get(self):

    #
    # welcome_template = jinja_current_dir.get_template("Templates/welcome1.html")
    # self.response.write(welcome_template.render())
  #   user = users.get_current_user()
  #   # If the user is logged in...
  #   if user:
  #     email_address = user.nickname()
  #     cssi_user = CssiUser.get_by_id(user.user_id())
  #     signout_link_html = '<a href="%s">sign out</a>' % (
  #         users.create_logout_url('/'))
  #     # If the user has previously been to our site, we greet them!
  #     if cssi_user:
  #       self.response.write('''
  #           Welcome %s %s (%s)! <br> %s <br>''' % (
  #             cssi_user.first_name,
  #             cssi_user.last_name,
  #             email_address,
  #             signout_link_html))
  #     # If the user hasn't been to our site, we ask them to sign up
  #     else:
  #       self.response.write('''
  #           Welcome to our site, %s!  Please sign up! <br>
  #           <form method="post" action="/">
  #           <input type="text" name="first_name">
  #           <input type="text" name="last_name">
  #           <input type="text" name="user_name">
  #           <input type="text" name="password">
  #           <input type="submit">
  #           </form><br> %s <br>
  #           ''' % (email_address, signout_link_html))
  #   # Otherwise, the user isn't logged in!
  #   else:
  #     self.response.write('''
  #       Please log in to use our site! <br>
  #       <a href="%s">Sign in</a>''' % (
  #         users.create_login_url('/')))
  #
  # def post(self):
  #   bye_template = jinja_current_dir.get_template("Templates/Home.html")
  #   self.response.write(bye_template.render())
  #   user = users.get_current_user()
  #   if not user:
  #     # You shouldn't be able to get here without being logged in
  #     self.error(500)
  #     return
  #   cssi_user = CssiUser(
  #       first_name=self.request.get('first_name'),
  #       last_name=self.request.get('last_name'),
  #       id=user.user_id())
  #   cssi_user.put()
  #   self.response.write('Thanks for signing up, %s!' %
  #       cssi_user.first_name)
  #
  # def post(self):
  #     username = self.request.get("user_name")
  #     newuser = CssiUser(user_name = username, last_activity = datetime.datetime.now())



    welcome_template = jinja_current_dir.get_template("Templates/signup_page.html")
    if self.request.cookies.get("loggen_in") == True:
        self.response.write(welcome_template.render(success =True, user = self.request.cookies.get("user")))

    else:
        self.response.write(welcome_template.render(failure = True))


    # welcome_template = jinja_current_dir.get_template("Templates/welcome1.html")
    # self.response.write(welcome_template.render())

    # welcome_template = jinja_current_dir.get_template("Templates/signup_page.html")
    # if self.request.cookies.get("loggen_in") == True:
    #     self.response.write(welcome_template.render(success =True, user = self.request.cookies.get("user")))

    # else:
    #     self.response.write(welcome_template.render(failure = True))

    # If the user s logged in...
class NewUserHandle(webapp2.RequestHandler):
  def post(self):
    home_template = jinja_current_dir.get_template("Templates/signup_page.html")
    cssi_user = CssiUser(
    first_name = self.request.get('firstName'),
    last_name = self.request.get('lastName'),
    username = self.request.get('Username'),
    email = self.request.get('Email'),
    password = self.request.get('Password'))
    # saved_info = self.request.get(''))

    cssi_user.put()
    self.response.set_cookie("logged_in", "True")
    self.response.set_cookie("user", cssi_user.username)
    self.response.write(home_template.render(success = True, user = cssi_user.first_name))
    sleep(.5)
    self.redirect('/Login')

class SignUpPageHandler(webapp2.RequestHandler):
    def get(self):
        content = jinja_current_dir.get_template("Templates/signup_page.html")
        # cssi_user = CssiUser(
        # first_name = self.request.get('firstName'),
        # last_name = self.request.get('lastName'),
        # username = self.request.get('Username'),
        # email = self.request.get('Email'),
        # password = self.request.get('Password'))
        #
        # cssi_user.put()
        # self.response.set_cookie("logged_in", "True")
        # self.response.set_cookie("user", cssi_user.username)
        # self.response.write(home_template.render(success = True, user = cssi_user.first_name))
        # sleep(.5)
        # self.redirect('/Login')
        self.response.write(content.render())
        # def post(self):



class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.delete_cookie("logged_in")
        self.response.delete_cookie("user")
        print('Hello')
        self.redirect('/')

# class Dashboard(ndb.Model):
#     button_save = ndb.StringProperty();
#     actual_name = ndb.StringProperty();


# class HomeWithDashboardPage(webapp2.RequestHandler):
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        session = jinja_current_dir.get_template("Templates/signIn_page.html")
        self.response.write(session.render(start = True, error = False))

    def post(self):
        username = self.request.get("Username")
        password = self.request.get("Password")

        session_iniciada = False
        q = CssiUser.query().fetch()
        print q
        for user in q:
            if username == user.username and password == user.password:
                print "Registers as correct"
                print username
                print password

                self.response.set_cookie("logged_in","True")
                self.response.set_cookie("user", user.username)
                self.response.clear()
                session_iniciada = True
                self.redirect('/Home')
                return

            if username != user.username and password != user.password:
                session_iniciada = False
                error = True
                self.response.delete_cookie("logged_in")
                self.response.delete_cookie("user")

        if not session_iniciada:
            not_session = jinja_current_dir.get_template("Templates/signIn_page.html")
            self.response.write(not_session.render(start = True, error = True, Username = username, Password = password))

        # else:
        #     self.redirect("/Home")


# class HomeWithDashboardPage(webapp2.RequestHandler):
#     def post(self):
#         home_template = jinja_current_dir.get_template("Templates/homePage.html")
#         answer = self.request.get('answer')
#         actual_name = self.request.get('submit')
#
#         SaveData = Dashboard(button_save = answer, actual_name = actual_name)
#         SaveData.put()
#         # self.response.write(home_template.render(button_save = answer, actual_name = actual_name))
#         self.redirect('/Home')
#         # time.sleep(.15)

# class LogoutHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.delete_cookie("logged_in")
#         self.response.delete_cookie("user")
#
#         self.redirect('/')

class Dashboard(ndb.Model):
    button_save = ndb.StringProperty();
    username = ndb.StringProperty();
    actual_name = ndb.StringProperty();


class HomePage(webapp2.RequestHandler):
    def get(self):
        username = self.request.cookies.get('user')
        home_template = jinja_current_dir.get_template("Templates/homePage.html")
        if username:
            intento = Dashboard.query(Dashboard.username == username).fetch()
            intento = filter(lambda x : x.actual_name, intento)
        else:
            intento = []
        print(intento)
        self.response.write(home_template.render(intento=intento, user=(username or 'Guest')))
    #def post(self):

        # if self.request.cookies.get("logged_in") == "True":
            # dashboardData = CssiUser.query()
            # self.response.write(home_template.render(active = True, dashboardData = dashboardData))
        # else:



    def post(self):
        answer = self.request.get('link')
        actual_name = self.request.get('actual_name')
        username = self.request.cookies.get('user')

        print Dashboard.username

        # print cssi_user.username

        if username:
            SaveData = Dashboard(button_save = answer, actual_name = actual_name, username = username)
            SaveData.put()
        self.redirect('/Home')
        time.sleep(.15)

class EducationPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/education.html")
        params = {
            'navbar_content': EDUCATION_NAV
            # [
            #     ("Daycare",  "DaycareandPreschool", "Daycare and Preschool"),
            #     # "Secondary School",
                # "Colleges and Universities",
                # "International Boarding Schools",
                # "Learning Resources"
            # ]
        }
        self.response.write(page_content.render(params))

class DaycarePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/daycare.html")
        self.response.write(page_content.render(navbar_content=EDUCATION_NAV))

class SecondaryPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/secondary.html")
        self.response.write(page_content.render(navbar_content=EDUCATION_NAV))

class CollegePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/college.html")
        self.response.write(page_content.render(navbar_content = EDUCATION_NAV))

class InternationalPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/intl.html")
        self.response.write(page_content.render(navbar_content = EDUCATION_NAV))

class LearningPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/learning.html")
        self.response.write(page_content.render(navbar_content = EDUCATION_NAV))

class ImmigrationPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/immigration.html")
        params = {
            'navbar_content': IMMIGRATION_NAV
        }
        self.response.write(page_content.render(params))

class LegalPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/legal.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))

class CitizenshipPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/citizenship.html")
        # navbar_content = jinja_current_dir.get_template("Templates/citizenship.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))

class VisaPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/visa.html")
        # navbar_content = jinja_current_dir.get_template("Templates/visa.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))

class StatePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/state.html")
        # navbar_content = jinja_current_dir.get_template("Templates/state.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))


class USLifePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/uslife.html")
        params = {
            'navbar_content':USLIFE_NAV
        }
        self.response.write(page_content.render(params))

class InsurancePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/insurance.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class HousingPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/housing.html")
        # navbar_content = jinja_current_dir.get_template("Templates/insurance.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class HealthCare(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/healthCare.html")
        # navbar_content = jinja_current_dir.get_template("Templates/healthCare.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class BankAndFinancial(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/financial.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class Employment(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/employment.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class CulturePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/culture.html")
        params = {
            'navbar_content': USCULTURE_NAV
        }
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class SlangPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/slang_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class EtiquettePage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/etiquette_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class PoliticalClimatePage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/politicalClimate_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class SportsPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/sports_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class HolidaysAndHistoryPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/holidaAndHistory.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class StateAttraction(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/stateAtractions_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class GeneralTipsPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/genTips_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

# class LogInPage(webapp2.RequestHandler):
#     def get(self):
#         login_content = jinja_current_dir.get_template("Templates/login_page.html")
#         self.response.write(login_content.render())


class ForumPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/forum.html")
        self.response.write(page_content.render())


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcomePage_content = jinja_current_dir.get_template("Templates/welcome1.html")
        self.response.write(welcomePage_content.render())

class AboutPage(webapp2.RequestHandler):
    def get(self):
        aboutPage_content = jinja_current_dir.get_template("Templates/about_page.html")
        self.response.write(aboutPage_content.render())
# app = webapp2.WSGIApplication([

  # ('/Home', HomeWithDashboardPage)
# class LoginPage(webapp2.RequestHandler):
#     def get(self):
#         login_content = jinja_current_dir.get_template("Templates/login_page.html")
#         self.response.write(login_content.render())
    # def post(self):
    #     print("hello")
    #     username = self.request.get("user_name")
    #     newuser = CssiUser(user_name = username, last_activity = datetime.datetime.now())

class DeletePage(webapp2.RequestHandler):
    def post(self):
        key = self.request.get("key")
        self.response.write(key)
        ndb.Key(urlsafe=key).delete()
        sleep(.5)
        self.redirect('/Home')
        # content = jinja_current_dir.get_template()



app = webapp2.WSGIApplication([
  ('/About', AboutPage),
  ('/Delete', DeletePage),
  ('/Login', LoginHandler),
  ('/LogOut', LogoutHandler),
  ('/', WelcomePage),
  ('/NewUser', NewUserHandle),
  ('/SignUp', SignUpPageHandler),
 # x ('/welcome', WelcomePage),
  ('/Home', HomePage),
  ('/Education', EducationPage),
  ('/Immigration', ImmigrationPage),
  ('/USLife', USLifePage),
  ('/USCulture', CulturePage),
  ('/DaycareandPreschool', DaycarePage),
  ('/SecondarySchool', SecondaryPage),
  ('/CollegesandUniversities', CollegePage),
  ('/InternationalandBoarding', InternationalPage),
  ('/LearningResources', LearningPage),
  ('/InsuranceP', InsurancePage),
  ('/HousingP', HousingPage),
  ('/HealthC', HealthCare),
  ('/BankFinan', BankAndFinancial),
  ('/Employ', Employment),
  ('/LegalResources', LegalPage),
  ('/CitizenshipInfo', CitizenshipPage),
  ('/VisaInfo', VisaPage),
  ('/StateInfo', StatePage),
  ('/SlangP', SlangPage),
  ('/EtiqP', EtiquettePage),
  ('/PolCliP', PoliticalClimatePage),
  ('/SportsP', SportsPage),
  ('/HolHisP', HolidaysAndHistoryPage),
  ('/StateAttrP', StateAttraction),
  ('/GenTips', GeneralTipsPage),
  ('/Forum', ForumPage),
  ('/formsubmit', FormSubmit),
  ('/questions', ShowQuestions),
], debug=True)
