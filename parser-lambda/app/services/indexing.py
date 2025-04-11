from clients import MarqoClient


class DocIndexer:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.marqo_client = MarqoClient(
            url="http://localhost:8882",
            index_name=index_name,
            model="hf/all-MiniLM-L6-v2",
            tensor_fields=["text"],
        )

    def index_data(self, data: dict, uid: str):
        self.uid = uid
        docs = self.__prepare_docs(data)
        print(f"Prepared documents for indexing: {docs}")

        marqo_res = self.marqo_client.index_documents(docs)
        print(marqo_res)

    def __prepare_docs(self, user_doc):
        docs = []
        for skill in user_doc.get("skills", []):
            docs.append(
                {
                    "_id": f"{self.uid}-{skill.get('name')}",
                    "uid": self.uid,
                    "type": "skill",
                    "context": skill.get("context"),
                    "recently_used": skill.get("last_used"),
                    "experience_years": skill.get("experience_years"),
                    "skill_name": skill.get("name"),
                    "text": f"{skill.get('experience_years', 'UNKNOWN')} years of experience in {skill.get('name')} (context: {skill.get('context')}) last used in {skill.get('last_used', 'UNKNOWN')}",  # this gets embedded
                }
            )

        for experience in user_doc.get("experience", []):
            docs.append(
                {
                    "_id": f"{self.uid}-{experience.get('role')}-{experience.get('company')}",
                    "uid": self.uid,
                    "type": "experience",
                    "role": experience.get("role"),
                    "company": experience.get("company"),
                    "start_date": experience.get("start_date"),
                    "end_date": experience.get("end_date"),
                    "text": f"{experience.get('role')} at {experience.get('company')} from {experience.get('start_date')} to {experience.get('end_date')}, skills used: {', '.join(experience.get('skills_used', []))}",  # this gets embedded
                }
            )
        for project in user_doc.get("projects", []):
            docs.append(
                {
                    "_id": f"{self.uid}-{project.get('title')}",
                    "uid": self.uid,
                    "type": "project",
                    "title": project.get("title"),
                    "description": project.get("description"),
                    "p_type": project.get("type"),
                    "start_date": project.get("start_date"),
                    "end_date": project.get("end_date"),
                    "text": f"{project.get('title')} ({project.get('type')}) from {project.get('start_date')} to {project.get('end_date')}, skills used: {', '.join(project.get('skills_used', []))}",  # this gets embedded
                }
            )
        return docs
