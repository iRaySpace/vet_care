## Vet Care

ERPNext App for Vet Care

**Customizations**

* Hospital Report: Shows the InPatient Records status
* Patient: Added weight, species, breed, chip ID, and neutered option
* Patient: Deceased field (disables the Patient document)
* Patient: Added Pet Relation for relation of the Patient (Pet) and the Customer (Owners)
* Patient: Hide irrelevant fields
* Patient: Added nutrition field under Risk Factors
* Patient: Overrided core set_only_once
* Vital Signs: Added mucuous membrane, and capillary refill time (CRT) field
* Vital Signs: Removed irrelevant descriptions
* Vital Signs: Hide irrelevant fields
* Vital Signs: Override naming series to VS-.##### (can be set under Vetcare Settings)
* Vital Signs: Added Make Encounter custom button
* Patient Appointment: Added owner field
* Inpatient Record: Added customer field
* Contact: Validate for phone numbers with plus sign (+) formats, no spaces
* Sales Invoice: Validate Customer if related to the Patient via Pet Relation
* DocTypes: Added Pet Relation (for Patient), Species (for Patient), Vetcare Settings (for core overrides)
* Print Formats: Added Euthanasia (for Patient), Procedure Consent (for Patient), and Veterinary Prescription (for Patient)
* Whitelisted methods: Overrided get_events (for Calendars), download_pdf (for PFs - calculate age function for Jinja)

#### License

MIT