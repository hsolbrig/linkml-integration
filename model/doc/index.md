
# integration


**metamodel version:** 1.7.0

**version:** 0.1.0


Testing harness for linkml integration testing


### Classes

 * [Comparator](Comparator.md) - Output comparator
 * [Filepath](Filepath.md) - a relative path to a file or directory
 * [Filter](Filter.md) - Pre comparison filters
 * [Manifest](Manifest.md) - A collection of Subsets, modules, comparators, and/or a manifest
 * [Module](Module.md) - LinkML software module to be tested
 * [Subset](Subset.md) - Categorization of type of test
 * [TestEntry](TestEntry.md) - A specific test to be executed in the context of a module
 * [TestSet](TestSet.md)

### Mixins


### Slots

 * [➞description](comparator__description.md) - comparator description
 * [➞entry_point](comparator__entry_point.md) - Comparator entry point
 * [➞name](comparator__name.md)
 * [➞is_directory](filepath__is_directory.md) - True means path is directory, false means file
 * [➞path](filepath__path.md)
 * [➞description](filter__description.md) - comparator description
 * [➞entry_point](filter__entry_point.md) - Filter entry point
 * [➞name](filter__name.md)
 * [➞comparators](manifest__comparators.md) - Comparators that can be referenced in the model
 * [➞description](manifest__description.md) - A description of the intent and purpose of a test set
 * [➞filters](manifest__filters.md) - Precomparison filters
 * [➞modules](manifest__modules.md) - Testing modules
 * [➞subsets](manifest__subsets.md) - Subsets used in the model
 * [➞tests](manifest__tests.md) - Actual test sets
 * [➞comparator](module__comparator.md) - Comparator to be used for the particular module's output
 * [➞description](module__description.md) - Description of the module
 * [➞entry_point](module__entry_point.md) - Module name and entry point
 * [➞filter](module__filter.md) - pre comparison filter to remove metadata, etc.
 * [➞name](module__name.md) - Unique module name
 * [➞skip](module__skip.md) - Skip this module if true
 * [➞subsets](module__subsets.md) - Subset(s) that this module belongs to
 * [➞description](subset__description.md) - Description of the particular subset
 * [➞name](subset__name.md) - name of specific subset
 * [➞description](testEntry__description.md) - Reason the test exists -- what it tests
 * [➞fail_text](testEntry__fail_text.md) - If present, string(s) that should be found in failure text
 * [➞issues](testEntry__issues.md) - Github issue(s) that the test addresses
 * [➞name](testEntry__name.md) - Name of the specific test.
 * [➞parameters](testEntry__parameters.md) - generator parameter string
 * [➞skip](testEntry__skip.md) - Skip this test if true
 * [➞source](testEntry__source.md) - source file or directory -- none if omitted
 * [➞subsets](testEntry__subsets.md) - Subset(s) that this particular test belongs to. Can be used as a filter
 * [➞target](testEntry__target.md) - target file or directory
 * [➞use_stdout](testEntry__use_stdout.md) - output appears on stdout.  Catch and redirect to the output file
 * [➞module](testSet__module.md) - module to be tested
 * [➞tests](testSet__tests.md) - collection of tests to be executed against the named module

### Enums


### Subsets


### Types


#### Built in

 * **Bool**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Pythonpath](types/Pythonpath.md)  ([String](types/String.md))  - A python style path
 * [Unixpath](types/Unixpath.md)  ([String](types/String.md))  - A unix style path
 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
