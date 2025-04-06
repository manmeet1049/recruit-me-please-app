import io
import re
import PyPDF2
from docx import Document


# TODO: identify the file from the magic number instead of the extension.
class ResumeParser:
    def __init__(self, file_content: bytes, filename: str):
        """
        :param file_content: File content in bytes
        :param filename: Filename with extension (used to determine format)
        """
        self.file_content = file_content
        self.filename = filename
        
        parsed_data = self.__parse()
        self.resume_content = parsed_data.get("text")
        self.resume_links = parsed_data.get("links")

        print(self.resume_content, "\n\n", self.resume_links)

    def __parse(self):
        _, file_extension = self.filename.lower().rsplit(".", 1)

        if file_extension == "docx":
            return self._parse_docx()
        elif file_extension == "txt":
            return self._parse_txt()
        elif file_extension == "pdf":
            return self._parse_pdf()
        else:
            raise ValueError(f"Unsupported file format: .{file_extension}")

    def _extract_links(self, text: str):
        link_pattern = r"https?://[^\s)]+"
        return re.findall(link_pattern, text)

    def _parse_docx(self):
        text = []
        links = []

        stream = io.BytesIO(self.file_content)
        doc = Document(stream)

        for paragraph in doc.paragraphs:
            paragraph_text = paragraph.text
            text.append(paragraph_text)

            paragraph_links = self._extract_links(paragraph_text)
            links.extend(paragraph_links)

        for rel in doc.part.rels.values():
            if (
                rel.reltype
                == "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
            ):
                links.append(rel._target)

        return {"text": "\n".join(text), "links": list(set(links))}

    def _parse_txt(self):
        text = self.file_content.decode("utf-8")
        links = self._extract_links(text)
        return {"text": text, "links": list(set(links))}

    def _parse_pdf(self):
        text = ""
        links = []

        stream = io.BytesIO(self.file_content)
        pdf_reader = PyPDF2.PdfReader(stream)

        for page in pdf_reader.pages:
            page_text = page.extract_text() or ""
            text += page_text

            if "/Annots" in page:
                for annot in page["/Annots"]:
                    annot_obj = annot.get_object()
                    if annot_obj.get("/A") and annot_obj["/A"].get("/URI"):
                        links.append(annot_obj["/A"]["/URI"])

        text_links = self._extract_links(text)
        links.extend(text_links)

        return {"text": text, "links": list(set(links))}
