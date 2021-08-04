sign_in_button = "//span[text()='Sign in to your account']/parent::a"
sign_in_email_box = "//*[@id='i0116']"
sign_in_password_box = "//*[@id='i0118']"
sign_in_next_button = "//*[@id='idSIButton9']"
delinquency_report_title = "//span[text()='60+ Delinquency Report ']"
page_background = ".displayArea.disableAnimations.fitToPage"  # css selector
# report_header = "//span[@class = 'textRun']/parent::p/parent::div"
report_header = "//span[@class = 'textRun']"
visual_container = "visualContainerHost"  # class name
visuals = "//div[contains(@class, 'visualContainer') and not(@aria-label='Power BI Report' or @aria-roledescription='Text box' or @role='img' or @aria-roleDescription='Slicer' or @aria-roleDescription='Button' or @aria-roleDescription='Image') and @aria-label]"
slicers = ".visual.visual-slicer"  # css selector
slicer_dropdown_popup = ".slicer-dropdown-popup.visual"  # css selector
slicer_checkboxes = "slicerCheckbox"  # class name
