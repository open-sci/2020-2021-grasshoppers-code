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

# DMP
## Classes of errors in DOI names: code
<blockquote>
Section 3.4.5: in case you have developed unit tests to check the correctness of the code, then you have a documented procedure for quality. However, I do not know if you did tests or not.
</blockquote>
<p>
The answer is no, the test driven development procedure has not been adopted. However, we think it would have been better to adopt it. Although TDD requires tests to be developed before code, we believe that it still has value to develop them afterwards, in order to have a solid foundation in case of extensions or code changes. For this reason, we developed unit tests, using the Python built-in "unittest" framework.
</p>
