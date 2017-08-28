class Forms:
    def __init__(self, slug):
        self.corp_slug = slug

    def getFormList(self):
        return Forms.object.filter(corporate__slug=self.corp_slug)
