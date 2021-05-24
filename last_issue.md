# General comments from the presentation

<blockquote>
You said that it is pretty impossible that the process stop to compute the various values. But what does it happen if someone by accident switch off your computer while running the computation? Do you have a way to restart it from the last data produced, avoiding to start it again from the beginning?
</blockquote>
<p>
Indeed, it is true, if the PC were to shut down the entire work (except for the cache of requests to the DOI Proxy server) would be lost. In order to deal with this problem, we have implemented a new support method, read_cache, which if a cache file has been created, reads the data processed up to that moment, in order to restart from the last CSV line read and not from the beginning. This function has been integrated in both check_dois_validity and procedures, that create or update a cache file every n DOIs. The number of DOIs after which to update the cache is customizable, as is the location of the cache file.
The code was inspired by the strategy adopted by the Leftovers 2.0 team to solve the same problem.
</p>
<blockquote>An invited expert identified a bug in the code for cleaning the DOIs. Is it possible that this bug affected the results presented? If so, it would be necessary to recompute the whole data, of course.</blockquote>
<p>
Yes, the results related to the application of regular expressions have to be recalculated and have been recalculated. However, the results relating to the verification of the previous validity of the DOIs do not have to be recalculated and have been reused, to speed up the process.
</p>

# Data Management Plan

## Title: Classes of errors in DOI names: output dataset
<blockquote>
Section 3.1.3: you have to specify the vocabulary used, avoiding the sentence "Couldn't find it? Insert it manually"
</blockquote>
<p>
In fact, although we determined the vocabulary, the phrase "Couldn't find it? Insert it manually" came to the fore in the pdf file. To prevent this, we have clarified which vocabulary we use, with specify section.
</p>


<blockquote>
Section 3.1.8: since you specified (in section 3.1.7) that you will use naming convention, you have to specify which naming convention is adopted.
</blockquote>
<p>
This part corrected and specified which naming convention is adopted.
</p>

<blockquote>
Section 3.1.9: here you should explain how to associate version numbers to your dataset, and not which version is currently in use.
</blockquote>
<p>
This section has also been checked and edited. We used Semantic Versioning 2.0.0 (https://semver.org/) for both datasets. 
</p>

<blockquote>
Section 4.4: the answer provided is "[Other]" but not additional comment has been added there to clarify what that "[Other]" means.
</blockquote>
<p>
The answer provided is "Other" We add an additional comment to clarify what that "Other" means. The data is available on Github Repository and Zenodo under an ISC license for re-use.
</p>

## Classes of errors in DOI names: code

<blockquote>
Section 2.1: in this context the term "data" should be interpreted as "software". Thus, the question refers to if you are going to reuse existing software for accomplishing your goal. Under this meaning, please be aware that also the Section 2.2 and Section 2.3 could be populated with some information. Please notice that this interpretation of "data" as "software" may affect also other points of the DMP.
</blockquote>
<p>
Despite the fact that we have answered these questions above, our responses are not visible due to an issue with the Argos platform.We have had Argos problems like this very often in a few questions. The answer for 2.2: ZENODO. Related to the question "Which data will be re-used": we responded, Citations to invalid DOI-identified entities obtained from processing DOI-to-DOI citations to add in COCI.
</p>


<blockquote>
Section 3.1.9: here you should explain how to associate version numbers to your dataset, and not which version is currently in use.
</blockquote>
<p>
The answer to this question has been modified. Semantic Versioning 2.0.0 (https://semver.org/) was used for both dataset.
</p>


<blockquote>
Section 3.1.15: I do not believe you use/share Python Compiled Files (.pyc) but rather simple Python files (.py), right?
</blockquote>
<p>
Since Python compiled files seems to be the only option, we saw it as suitable. We corrected this by using the description section.
</p>

<blockquote>
Section 3.4.5: in case you have developed unit tests to check the correctness of the code, then you have a documented procedure for quality. However, I do not know if you did tests or not.
</blockquote>
<p>
The answer is no, the test driven development procedure has not been adopted. However, we think it would have been better to adopt it. Although TDD requires tests to be developed before code, we believe that it still has value to develop them afterwards, in order to have a solid foundation in case of extensions or code changes. For this reason, we developed unit tests, using the Python built-in "unittest" framework.
</p>

# Protocol
<blockquote>
  "The data needed for this work is provided by COCI as a CSV": it is not provided by COCI (which is a collection), it is provided by myself.
</blockquote>
<p>
In our protocol we removed all the mentions of COCI as provider of the dataset and we substituted them with the reference to the Zenodo repository.
</p>
<blockquote>
  "The records are provided on public licence by": change in "license in" and put the bibliographic reference in a shape it is clear (e.g. by using italic or other appropriate format).
</blockquote>
<p>
The text was corrected as suggested and we put the full citation to the Zenodo repository of the dataset.
</p>
<blockquote>
 "40'228": write "40,228" (the comma in English notation is visual separator).
</blockquote>
<p>
As suggested, we used a comma instead of an apostrophe as visual separator for groups of thousands.
</p>
<blockquote>
  "there are two main classes of errors: author errors, made by authors when creating the list of cited articles for their publication, and database mapping errors, related to a data-entry error": it would be good to acknowledge here the fact that we have, in general, "human errors", i.e. those introduced by authors, editors and publisher representatives when managing the references - as explained during the workshop event.
</blockquote>
<p>
In the newer version of the protocol we described the class of "human-made" errors in addition to the two ("author errors" and "database-mapping errors") proposed in (Franceschini et al., 2015). Moreover we removed any mention to an adoption of the forementioned taxonomy in our methodology since our research question was not focused on the origin of errors present in DOIs but merely in their types and characteristics. 
</p>
<blockquote>
  "we manually isolated from a subset of 100 DOIs recurrent strings": how did you selected such 100 DOIs?
</blockquote>
<p>
Since we didn't store the subset of 100 DOIs from which we extracted recurrent patterns of errors and we were not able to reproduce it, we removed any mention to this subset of DOIs and we limited ourselves to state that we did a manual identification of a subset of recurrent strings which corrupted DOI prefixes and suffixes.
</p>
<blockquote>
  "eventual unwanted characters": remove "eventual"
</blockquote>
<p>
We removed the occurrence of the word "eventual" in section 3.3 of the newer version of the protocol.
</p>


# Article
<p>All the mentioned issues have been addressed, correcting former inconsistencies and mistakes. In addition, the article has been updated with new content, including descriptions of the added methods applied to improve the research.</p>

