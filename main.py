#### Python 3.8
#### All I ask is add "Login Template by @Skainetrobotics" to your finished code somewhere.
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
import requests
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd import app
from kivymd.theming import ThemeManager
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.properties import StringProperty
import time
import threading



class LoginScreen(Screen):
    response= StringProperty()
    Tries = 3
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
    
    def Login(self,user,password):
        
        if self.Tries != 0:
            
            user,password = self.Insecure_Login(user,password)
            if user == True and password== True:
                MainApp.Change_Screen(self.parent,screenname='HomeScreen')
            elif  len(user) == 0 and len(password) == 0:
                self.response = 'Please enter an ID and Password'
                MainApp.Error(self=self.parent,Message='Please enter an ID and Password')
                self.Tries -=1
                #MainApp.Change_Screen(self.parent,screenname='HomeScreen') ## use this if you just want to login with no password
            elif len(user) == 0 and len(password) > 0:
                self.response = 'Please enter an ID'
                MainApp.Error(self=self.parent,Message='Please enter an ID')
                self.Tries -=1
                
            elif len(password) == 0 and len(user) > 0:
                self.response = 'Please enter a password'
                MainApp.Error(self=self.parent,Message='Please Enter Password')
                self.Tries -=1
                
            else:
                self.response = 'Please try again'
                Snackbar(text="Please try again",snackbar_x="10",snackbar_y="10",size_hint_x=1,).open()
                self.Tries -=1
                
        else:
            ## Send text :D
            time.sleep(10)
            exit()
    
    def Registration(self):
        print('Registration button pressed')
        
    
    def Forgot_Password(self):
        print('Lost button pressed')   




    def Insecure_Login(self,user,password):
        Database_Result = MainApp.Get_Database_Info(self,path='Users')
        
        result = list(Database_Result)
        for res in result:
            if user == res:
                if Database_Result[user]['password'] == password:
                    user,password = True,True
                    return user,password
                else:
                    pass
             
       
        return user,password








 

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    StopCalled = False
                
    def Release_Drawer(self):
        MDNavigationDrawer.enable_swiping = True

    def Populate(self,Message):
        print('trying to print message')
        print(Message)
        Message = '100'
        
              
        viewer = self.ids['Grid_Layout']
        viewer.add_widget(MDLabel(text='View'))
            
    def Stop(self,question):
        self.StopCalled = True    
       
       
        
        
    def pressed(self, question, Product_Screen_Name):
            app = MDApp.get_running_app()
            app.Change_Screen(Product_Screen_Name)
            
    
    def callback(self, instance):
        pass
        
    def FooterSection():
        pass

   
       
    
    def ThreadOneExecute(self):
        print('Button1 Pressed')
        for x in range(1,1009090,2):
            time.sleep(3)
            print(x)
            viewer = self.ids['Grid_Layout']
            viewer.add_widget(MDLabel(text=str(x)))
        print('Button1 finished')
    
    def ThreadTwoExecute(self):
        self.StopCalled = False
        print('Button2 Pressed')
        numb = 1
        while self.StopCalled == False:
            print("Thread two %i" %numb)
            Text = "Thread two %i" %numb
            viewer = self.ids['Grid_Layout']
            viewer.add_widget(MDLabel(text=Text))
            numb +=1
            time.sleep(1)
        print('Button2 finished')
        

########################    MAIN CLASSES    #######################################

class ContentNavigationDrawer(BoxLayout):
    
    def Toggle_Nav_Drawer(self,q):
        try:
            MDNavigationDrawer.set_state(self.root_window.nav_drawer,new_state='toggle')
        except:
            MDNavigationDrawer.set_state(self = self.root.ids.nav_drawer,new_state='toggle')
            
        
        
        
        


class WindowManager(ScreenManager):
    pass



class MainApp(MDApp): 
    def __init__(self,*args,**kwargs):
        super(MainApp,self).__init__(*args,**kwargs)
        theme_cls = ThemeManager()
        ############################ Take this out when compiling if for phone... But this isnt fit for phone
        Window.size = (800, 400)
        ###########################
        self.theme_cls.primary_palette = 'Gray'
        self.sm=WindowManager()

    def Change_Screen(self,screenname):
        try:
            screenmanager = self.root.ids['screen_manager']
            screenmanager.current = screenname
        except:
            self.current = screenname
        
    
   
    def ToolBar(self,page):
        anchor_layout = AnchorLayout(
            anchor_x= 'center',
            anchor_y= 'top')
        toolbar = MDToolbar(
            title="Threading",
            md_bg_color=self.theme_cls.primary_color,
            background_palette="Primary",
            background_hue="700",
            elevation=10,
            type= "top",
        )
        
        toolbar.left_action_items = [["menu", lambda x: ContentNavigationDrawer.Toggle_Nav_Drawer(self,q=0)]]
        #toolbar.right_action_items = [["menu", lambda x: ContentNavigationDrawer.Toggle_Nav_Drawer(self,q=0)]] ### add this for a right bar and add a class for it
        anchor_layout.add_widget(toolbar)  
        page.add_widget(anchor_layout)
         
    def Get_Database_Info(self,path):
        ### ADD A RECORD IN YOUR FIREBASE Named Users, with name of user as record and a sub record named password
        #Users
        #   |-Vampirebat
        #           |-password      Skainetrobotics
        try:
            Database_Url = 'https://YOURFIREBASEURLHERE.firebaseio.com/%s/.json' %(path)
            Database_Result = requests.get(Database_Url).json()
            return Database_Result
            
        except:
            MainApp.Error(self)
            MainApp.Change_Screen(self.parent,screenname='HomeScreen')
            
            

    def Error(self,Message):
        Snackbar(text=Message,snackbar_x="10",snackbar_y="10",size_hint_x=.9,).open()
    

def starter():
    if __name__ == '__main__':
        MainApp().run()


threading.Thread(target = starter()).start()



