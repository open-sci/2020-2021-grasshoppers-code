# General comments from the presentation

<blockquote>
You said that it is pretty impossible that the process stop to compute the various values. But what does it happen if someone by accident switch off your computer while running the computation? Do you have a way to restart it from the last data produced, avoiding to start it again from the beginning?
</blockquote>
<p>
Indeed, it is true, if the PC were to shut down the entire work (except for the cache of requests to the DOI Proxy server) would be lost. In order to deal with this problem, we have implemented a new support method, read_cache, which if a cache file has been created, reads the data processed up to that moment, in order to restart from the last CSV line read and not from the beginning. This function has been integrated in both check_dois_validity and procedures, that create or update a cache file every n DOIs. The number of DOIs after which to update the cache is customizable, as is the location of the cache file.
The code was inspired by the strategy adopted by the Leftovers 2.0 team to solve the same problem.
</p>
<blockquote>An invited expert identified a bug in the code for cleaning the DOIs. Is it possible that this bug affected the results presented? If so, it would be necessary to recompute the whole data, of course.</blockquote>
<img src="https://i.kym-cdn.com/entries/icons/original/000/028/596/dsmGaKWMeHXe9QuJtq_ys30PNfTGnMsRuHuo_MUzGCg.jpg" alt="Well yes, but actually no meme">
<p>
Yess, the results related to the application of regular expressions have to be recalculated and have been recalculated. However, the results relating to the verification of the previous validity of the DOIs do not have to be recalculated and have been reused, to speed up the process.
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


# Article
<p>All the mentioned issues have been addressed, correcting former inconsistencies and mistakes. In addition, the article has been updated with new content, including descriptions of the added methods applied to improve the research.</p>

