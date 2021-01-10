#;encoding=utf-8
# Example file to redact Social Security Numbers from the
# text layer of a PDF and to demonstrate metadata filtering.

import re
from datetime import datetime

import pdf_redactor

## Set options.

options = pdf_redactor.RedactorOptions()

options.metadata_filters = {
	# Perform some field filtering --- turn the Title into uppercase.
	"Title": [lambda value : value],

	# Set some values, overriding any value present in the PDF.
	"Producer": [lambda value : value],
	"CreationDate": [lambda value : value],

	# Clear all other fields.
	"DEFAULT": [lambda value : None],
}

# Clear any XMP metadata, if present.
options.xmp_filters = [lambda xml : None]

# Redact things that look like social security numbers, replacing the
# text with X's.
options.content_filters = [
	# First convert all dash-like characters to dashes.
	(
		re.compile(u"[−–—~‐]"),
		lambda m : "-"
	),

	# Then do an actual SSL regex.
	# See https://github.com/opendata/SSN-Redaction for why this regex is complicated.
	(
		re.compile(r"[0-9]{2} [0-9]{2} [0-9]{3} [0-9]{3} [0-9]{3}"),
		lambda m : "00 00 000 000 000"
	),
	
	(
		re.compile(r"[0-9]{2} [0-9]{2} [0-9]{7} [0-9]{2}"),
		lambda m : "00 00 0000000 00"
	),

	(
		
		re.compile(r"[0-9]{3} *[A-Z][0-9]{5} [A-Z]"),
		lambda m : "000 A00000 A"
	),
	( 
		re.compile("[A-Z]* [0-9]{4} [A-Z0-9]{6}"),
		lambda m: "---"
	),
	(
		re.compile(r"[0-9]{3} [0-9]{2} [0-9]{3} [0-9]{3} [0-9]{3} [0-9]{3} [A-Z] [A-Z]"),
		lambda m: "000 00 000 000 000 000 A A"
	)
]

# Filter the link target URI.
options.link_filters = [
	lambda href, annotation : "https://www.google.com" 
]

# Perform the redaction using PDF on standard input and writing to standard output.
pdf_redactor.redactor(options)
