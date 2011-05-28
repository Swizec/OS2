import wx

def get_folder():
    app = wx.PySimpleApp()
    dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        pass#print dialog.GetPath()
    dialog.Destroy()
    return dialog.GetPath()