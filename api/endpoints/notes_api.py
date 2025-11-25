from api.endpoints.base_api import BaseApi

class NotesApi(BaseApi):
    def create_note(self, data):
        return self.post("/notes", data)

    def get_all_notes(self):
        return self.get("/notes")

    def get_note(self, note_id):
        return self.get(f"/notes/{note_id}")

    def update_note(self, note_id, data):
        return self.put(f"/notes/{note_id}", data)

    def update_status_note(self, note_id, data):
        return self.patch(f"/notes/{note_id}", data)

    def delete_note(self, note_id):
        return self.delete(f"/notes/{note_id}")
