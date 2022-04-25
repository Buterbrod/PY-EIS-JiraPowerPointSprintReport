# # PowerPoint Library: Python-pptx
# import os
# from pptx import Presentation
# import shutil
#
# class PPTXPowerPoint:
#     def __init__(self, pptx_file, pptx_new_file):
#         self.pptx_file = pptx_file
#         self.pptx_new_file = pptx_new_file
#         # copy template to the new file
#         #self.copy_template(pptx_file, pptx_new_file)
#         # create pptx presentation object
#         # self.prs = Presentation(self.pptx_new_file)
#
#     def copy_template(self):
#         shutil.copyfile(self.pptx_file, self.pptx_new_file)
#
#     def duplicate_slide(self, index):
#         prs = self.prs
#         # specify the slide you want to copy the contents from
#         src_slide = prs.slides[index]
#         # Define the layout you want to use from your generated pptx
#         try:
#             blank_slide_layout = prs.slide_layouts[12]
#         except:
#             blank_slide_layout = prs.slide_layouts[len(prs.slide_layouts)]
#         # create now slide, to copy contents to
#         copied_slide = prs.slides.add_slide(blank_slide_layout)
#         # create images dict
#         imgDict = {}
#         # now copy contents from external slide, but do not copy slide properties
#         # e.g. slide layouts, etc., because these would produce errors, as diplicate
#         # entries might be generated
#         for shp in src_slide.shapes:
#             if 'Picture' in shp.name:
#                 # save image
#                 with open(shp.name + '.jpg', 'wb') as f:
#                     f.write(shp.image.blob)
#                 # add image to dict
#                 imgDict[shp.name + '.jpg'] = [shp.left, shp.top, shp.width, shp.height]
#             else:
#                 # create copy of elem
#                 el = shp.element
#                 newel = prs.copy.deepcopy(el)
#                 # add elem to shape tree
#                 copied_slide.shapes._spTree.insert_element_before(newel, 'p:extLst')
#         # add pictures
#         for k, v in imgDict.items():
#             copied_slide.shapes.add_picture(k, v[0], v[1], v[2], v[3])
#             os.remove(k)
#
#     def write_sprint_issues(self, sprint_issues):
#          for i in range(0, len(sprint_issues)):
#              self.duplicate_slide(self, 0)
#              self.write_issue_fields_on_slide(self.prs.slides[i+1], sprint_issues[i])
#          self.prs.save()
#
#     def write_issue_fields_on_slide(self, slide, issue_fields):
#          # -----------------------------------------------------------------------------------------------------
#          if "RMAP Link" in issue_fields:
#              slide.shapes[0].text_frame.paragraphs[0].runs[1].text = issue_fields["RMAP Link"]["Issue"].replace("RMAP", "")
#              slide.shapes[0].text_frame.paragraphs[0].runs[1].hyperlink.address = issue_fields["RMAP Link"]["Issue Link"]
#              # -----------------------------------------------------------------------------------------------------
#              slide.shapes[0].text_frame.paragraphs[0].runs[2].text = " " + issue_fields["RMAP Link"]["Issue Summary"]
#          else:
#              slide.shapes[0].text_frame.paragraphs[0].runs[1].text = ""
#              slide.shapes[0].text_frame.paragraphs[0].runs[1].hyperlink.address = ""
#              # -----------------------------------------------------------------------------------------------------
#              slide.shapes[0].text_frame.paragraphs[0].runs[2].text = ""
#          # -----------------------------------------------------------------------------------------------------
#          if "Epic Link" in issue_fields:
#              slide.shapes[0].text_frame.paragraphs[0].runs[3].text = issue_fields["Epic Link"]["Issue"]
#              slide.shapes[0].text_frame.paragraphs[0].runs[3].hyperlink.address = issue_fields["Epic Link"]["Issue Link"]
#              # -----------------------------------------------------------------------------------------------------
#              slide.shapes[0].text_frame.paragraphs[0].runs[5].text = issue_fields["Epic Link"]["Issue Summary"]
#          # -----------------------------------------------------------------------------------------------------
#          slide.shapes[2].text_frame.paragraphs[0].runs[0].text = issue_fields["Issue"]
#          slide.shapes[2].text_frame.paragraphs[0].runs[0].hyperlink.address = issue_fields["Issue Link"]
#          # -----------------------------------------------------------------------------------------------------
#          slide.shapes[2].text_frame.paragraphs[0].runs[1].text = issue_fields["Issue Summary"]
#          # -----------------------------------------------------------------------------------------------------
#          slide.shapes[2].text_frame.paragraphs[1].runs[0].text = issue_fields["Scope Summary"]
#          # -----------------------------------------------------------------------------------------------------
#          slide.shapes[2].text_frame.paragraphs[2].runs[0].text = "Issue Status: " + issue_fields["Status"]
#          # -----------------------------------------------------------------------------------------------------
#
# #     # def write_issue_fields_on_slide(self, slide, issue_fields):
# #     #     # -----------------------------------------------------------------------------------------------------
# #     #     slide.shapes[0].text_frame.paragraphs[0].runs[0].text = issue_fields["Issue"]
# #     #     slide.shapes[0].text_frame.paragraphs[0].runs[0].hyperlink.address = issue_fields["Issue Link"]
# #     #     # -----------------------------------------------------------------------------------------------------
# #     #     slide.shapes[0].text_frame.paragraphs[0].runs[1].text = " " + issue_fields["Issue Summary"]
# #     #     # -----------------------------------------------------------------------------------------------------
# #     #     slide.shapes[2].text_frame.paragraphs[0].runs[1].text = issue_fields["Wiki Ticket Summary Link"]
# #     #     slide.shapes[2].text_frame.paragraphs[0].runs[1].hyperlink.address = issue_fields["Wiki Ticket Summary Link"]
# #     #     # -----------------------------------------------------------------------------------------------------
# #     #     slide.shapes[2].text_frame.paragraphs[1].runs[0].text = issue_fields["Scope Summary"]
# #     #     # -----------------------------------------------------------------------------------------------------
# #     #     # slide.shapes[2].text_frame.paragraphs[2].runs[1].text = issue_fields["Story Points"]
# #     #     # -----------------------------------------------------------------------------------------------------
# #     #     slide.shapes[2].text_frame.paragraphs[3].runs[0].text = issue_fields["User Story"]
# #     #     # -----------------------------------------------------------------------------------------------------
#
