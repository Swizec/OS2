import wx

class TextFrame(wx.Frame):
    
    callback = "not set"
    
    def __init__(self):
        
        wx.Frame.__init__(self, None, -1, 'New repository info', size=(300, 150))
        panel = wx.Panel(self, -1)
        
        repnLabel = wx.StaticText(panel, -1, "Repository ID:")
        self.repn = wx.TextCtrl(panel, -1, '', size=(175, -1))
        
        self.repn.SetInsertionPoint(0)
        
        userLabel = wx.StaticText(panel, -1, "Username:")
        self.user = wx.TextCtrl(panel, -1, '', size=(175, -1))
        
        pwdLabel = wx.StaticText(panel, -1, "Password:")
        self.pwd = wx.TextCtrl(panel, -1, '', size=(175, -1),style=wx.TE_PASSWORD)
        
        btn = wx.Button(panel, label='Create', pos=(200, 80), size=(80,25))
        btn.Bind(wx.EVT_BUTTON, self.read)
        
        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        sizer.AddMany([repnLabel, self.repn, userLabel, self.user, pwdLabel, self.pwd, btn])
        panel.SetSizer(sizer)
    
    def read(self, event):
        self.callback([
            self.repn.GetValue(),
            self.user.GetValue(),
            self.pwd.GetValue()])
        self.Close()
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TextFrame()
    frame.Show()
    app.MainLoop()
    
    