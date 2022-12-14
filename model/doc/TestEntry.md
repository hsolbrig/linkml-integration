
# Class: TestEntry


A specific test to be executed in the context of a module

URI: [test:TestEntry](https://linkml.org/testing/TestEntry)


[![img](images/TestEntry.svg)](images/TestEntry.svg)

## Referenced by Class

 *  **None** *[➞tests](testSet__tests.md)*  <sub>0..\*</sub>  **[TestEntry](TestEntry.md)**

## Attributes


### Own

 * [➞description](testEntry__description.md)  <sub>0..1</sub>
     * Description: Reason the test exists -- what it tests
     * Range: [String](types/String.md)
 * [➞issues](testEntry__issues.md)  <sub>0..\*</sub>
     * Description: Github issue(s) that the test addresses
     * Range: [String](types/String.md)
 * [➞source](testEntry__source.md)  <sub>0..1</sub>
     * Description: source file or directory -- none if omitted
     * Range: [Filepath](Filepath.md)
 * [➞target](testEntry__target.md)  <sub>1..1</sub>
     * Description: target file or directory
     * Range: [Filepath](Filepath.md)
 * [➞parameters](testEntry__parameters.md)  <sub>0..1</sub>
     * Description: generator parameter string
     * Range: [String](types/String.md)
 * [➞use_stdout](testEntry__use_stdout.md)  <sub>0..1</sub>
     * Description: output appears on stdout.  Catch and redirect to the output file
     * Range: [Boolean](types/Boolean.md)
 * [➞fail_text](testEntry__fail_text.md)  <sub>0..\*</sub>
     * Description: If present, string(s) that should be found in failure text
     * Range: [String](types/String.md)
 * [➞subsets](testEntry__subsets.md)  <sub>0..\*</sub>
     * Description: Subset(s) that this particular test belongs to. Can be used as a filter
     * Range: [Subset](Subset.md)
 * [➞skip](testEntry__skip.md)  <sub>0..1</sub>
     * Description: Skip this test if true
     * Range: [Boolean](types/Boolean.md)
