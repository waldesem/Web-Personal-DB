class Pagination:

    def __init__ (self, query, pagination, page):
        self.query = query.all()
        self.pagination = pagination 
        self.page = page
        self.start_index = self.pagination*(self.page-1)
        self.end_index = self.pagination*self.page
        self.results = self.query[self.start_index:self.end_index]
        
    def paginate (self):
        if self.page:
            return self.results
    
    def has_prev(self):
        if self.page < 2:
            return False
        prev_items = self.query[self.start_index-1:self.end_index]
        return True if len(self.results) < len(prev_items) else False

    def has_next(self):
        next_items = self.query[self.start_index:self.end_index+1]
        return True if len(self.results) < len(next_items) else False

