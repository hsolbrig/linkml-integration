
# Class: Module


LinkML software module to be tested

URI: [test:Module](https://linkml.org/testing/Module)


[![img](images/Module.svg)](images/Module.svg)

## Referenced by Class

 *  **None** *[➞modules](manifest__modules.md)*  <sub>0..\*</sub>  **[Module](Module.md)**
 *  **None** *[➞module](testSet__module.md)*  <sub>1..1</sub>  **[Module](Module.md)**

## Attributes


### Own

 * [➞name](module__name.md)  <sub>1..1</sub>
     * Description: Unique module name
     * Range: [String](types/String.md)
 * [➞description](module__description.md)  <sub>0..1</sub>
     * Description: Description of the module
     * Range: [String](types/String.md)
 * [➞entry_point](module__entry_point.md)  <sub>1..1</sub>
     * Description: Module name and entry point
     * Range: [Pythonpath](types/Pythonpath.md)
     * Example: YAMLLoader.load_any None
 * [➞filter](module__filter.md)  <sub>0..1</sub>
     * Description: pre comparison filter to remove metadata, etc.
     * Range: [Filter](Filter.md)
 * [➞comparator](module__comparator.md)  <sub>0..1</sub>
     * Description: Comparator to be used for the particular module's output
     * Range: [Comparator](Comparator.md)
 * [➞subsets](module__subsets.md)  <sub>0..\*</sub>
     * Description: Subset(s) that this module belongs to
     * Range: [Subset](Subset.md)
 * [➞skip](module__skip.md)  <sub>0..1</sub>
     * Description: Skip this module if true
     * Range: [Boolean](types/Boolean.md)
