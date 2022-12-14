
# Class: Manifest


A collection of Subsets, modules, comparators, and/or a manifest

URI: [test:Manifest](https://linkml.org/testing/Manifest)


[![img](images/Manifest.svg)](images/Manifest.svg)

## Attributes


### Own

 * [➞description](manifest__description.md)  <sub>0..1</sub>
     * Description: A description of the intent and purpose of a test set
     * Range: [String](types/String.md)
 * [➞subsets](manifest__subsets.md)  <sub>0..\*</sub>
     * Description: Subsets used in the model
     * Range: [Subset](Subset.md)
 * [➞comparators](manifest__comparators.md)  <sub>0..\*</sub>
     * Description: Comparators that can be referenced in the model
     * Range: [Comparator](Comparator.md)
 * [➞filters](manifest__filters.md)  <sub>0..\*</sub>
     * Description: Precomparison filters
     * Range: [Filter](Filter.md)
 * [➞modules](manifest__modules.md)  <sub>0..\*</sub>
     * Description: Testing modules
     * Range: [Module](Module.md)
 * [➞tests](manifest__tests.md)  <sub>0..\*</sub>
     * Description: Actual test sets
     * Range: [TestSet](TestSet.md)
