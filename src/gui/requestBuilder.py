'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI dialog for building a search request
'''

import wx
import wx.richtext as rt
class condition:
    field=None
    cond_type=None
    criteria=None
    def __init__(self,field,cond_type,criteria):
        self.field=field
        self.cond_type=cond_type
        self.criteria=criteria

class builder(wx.Dialog):
    '''
    GUI dialog for addition of a file into the database
    '''


    #===========================================================================
    # constructor (building gui)
    #===========================================================================
    operators=(('and','and'),('or','or'),('or (exclusive)','xor'))
    fields=(('any field','any'),('title','title'),('description','description'),('tags','tags'),('document date','documentDate'),('Registering date','registeringDate'))
    conditions_text=(('sounds like','%s'),('spells exactly',"'%s'"))
    conditions_date=(('is before','<%s'),('is on or before','<=%s'),('is after','>%s'),('is on or after','>=%s'),('is on','='))
    conditions=[]
    def __init__(self,parent):
        '''
        Constructor
        '''
        
        wx.Dialog.__init__(self, parent, -1, _('Generation of a search request'),style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        self.totSizer = wx.GridBagSizer(4,2)
        
        explanations = _('In the following, enter the list of restriction defining your search request\n')
        explanations += _('Click on a condition to change it\n')
        explanations += _('Click on the + button to add another condition after the corresponding line\n')
        explanations += _('Click on the [+] button to add another group of conditions after the corresponding line\n')
        explanations += _('Click on the - button to remove the condition on the corresponding line\n')
        explanations += _('Click on the - button to remove the group of conditions for the corresponding line')
        self.totSizer.Add(wx.StaticText(self.panel,-1,explanations,style=wx.TE_MULTILINE),(0,0),span=(1,4),flag=wx.ALIGN_TOP|wx.EXPAND)
        #self.lstField = wx.ComboBox(self.panel,-1)
        #self.lstField.SetItems([x[0] for x in self.fields])
        #self.lstCondition = wx.ComboBox(self.panel,-1)
        #self.lstCondition.SetItems([x[0] for x in self.conditions_text])
        #self.lstCriteria = wx.TextCtrl(self.panel,-1)
        self.rtHuman     = rt.RichTextCtrl(self.panel,-1,style=wx.TE_AUTO_URL)
        self.rtHuman.SetEditable(False)
        self.rtHuman.GetCaret().Hide()
        
        #self.totSizer.Add(self.lstField,(1,1),flag=wx.EXPAND)
        #self.totSizer.Add(self.lstCondition,(1,2),flag=wx.EXPAND)
        #self.totSizer.Add(self.lstCriteria,(1,3),flag=wx.EXPAND)
        self.totSizer.Add(self.rtHuman,(1,0),span=(1,4),flag=wx.EXPAND)
        
        self.totSizer.AddGrowableCol(0)
        self.totSizer.AddGrowableRow(1)
        
        self.generateHuman()

        self.panel.SetSizerAndFit(self.totSizer)
        self.totSizer.Fit(self)
        self.SetSize((600,350))
        
        self.rtHuman.Bind(wx.EVT_TEXT_URL,self.onURLclick)
    def onURLclick(self,event):
        print "Condition : "+event.GetString()
    def generateHuman(self):
        urlStyle = rt.TextAttrEx()
        urlStyle.SetTextColour(wx.BLUE)
        #urlStyle.SetFontUnderlined(True)
        self.rtHuman.Clear()
        if len(self.conditions)<1:
            levelStr='0'
            self.rtHuman.BeginURL(levelStr)
            self.rtHuman.WriteText(_('All documents (no conditions)'))
            self.rtHuman.EndURL()
            self.rtHuman.WriteText('   ')
            self.rtHuman.BeginStyle(urlStyle)
            self.rtHuman.BeginURL(levelStr+' +')
            self.rtHuman.WriteText('+')
            self.rtHuman.EndURL()
            self.rtHuman.WriteText('   ')
            self.rtHuman.BeginURL(levelStr+' ++')
            self.rtHuman.WriteText('[+]')
            self.rtHuman.EndURL()
            self.rtHuman.WriteText('   ')
            self.rtHuman.BeginURL(levelStr+' -')
            self.rtHuman.WriteText('-')
            self.rtHuman.EndURL()
            self.rtHuman.WriteText('   ')
            self.rtHuman.BeginURL(levelStr+' --')
            self.rtHuman.WriteText('[-]')
            self.rtHuman.EndURL()
            self.rtHuman.EndStyle()

