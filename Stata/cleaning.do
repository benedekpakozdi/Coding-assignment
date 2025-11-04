**** Data cleaning *****

cd "C:\Users\Pakozdi_Benedek\Desktop\Coding for economics\assignment\Stata\data"

import delimited "raw/airbnb_london_listing.csv", varnames(1) bindquotes(strict) encoding("utf-8") clear

describe
brows

*lets check whether the locations are appear correctly:
tabulate country // we only have the UK which is great

describe market
tabulate market
** As we have different markets we should drop them

keep if market == "London"

** we can see that there is a big mess around the variable tpyes and their values
** As we are interested in the price and the possible effects of the accomodation related information, host's charactheristics, so lets dropp the unneccessary variables:

keep id host_id host_response_rate host_is_superhost host_has_profile_pic host_identity_verified is_location_exact property_type room_type accommodates bathrooms bedrooms beds bed_type price extra_people minimum_nights instant_bookable cancellation_policy review_scores_location review_scores_value number_of_reviews

** now we can see that there are varaibles that take true and false values, lets transform them first


replace host_has_profile_pic = "1" if host_has_profile_pic == "t"
replace host_has_profile_pic = "0" if host_has_profile_pic == "f"
destring host_has_profile_pic, replace

describe


** we can do this for all the binary variables 

foreach var in host_is_superhost host_identity_verified is_location_exact instant_bookable {
    replace `var' = "1" if `var' == "t"
    replace `var' = "0" if `var' == "f"
    destring `var', replace
}

describe

** now lets modify the host_response_rate 

replace host_response_rate = subinstr(host_response_rate, "%", "", .)
replace host_response_rate ="" if host_response_rate == "N/A"
destring host_response_rate, replace

replace host_response_rate = host_response_rate/100

** now lets modify the room and review related variables

foreach var in bathrooms bedrooms beds review_scores_location review_scores_value {
    replace `var' ="" if `var'== "NA"
    destring `var', replace
}


** and finally we only need to change the prices so they are numeric variables


foreach var in price extra_people {
    replace `var' = subinstr(`var', ",", "", .)   
    replace `var' = subinstr(`var', "$", "", .)   
    destring `var', replace                   
}


** now we should check wether are there any unrealistic observations that distort the data

/* let's see prices first */

summarize price

tabulate price

* lets drop prices over 1000 dollars as they are very unlikely that I would pay that much

keep if price < 1000

* now lets check the reviews

summarize review_scores_location review_scores_value
* they are all between 1-10 so that considered accurate

tabulate host_response_rate

*lets drop the hosts who don't reply back meaning that the resons rate is 0

drop if host_response_rate == 0

** and finally drop all the missing values

codebook

drop if missing(host_response_rate) /// we can see that this variable have the most amount of missing values

/* still missing for the following varaibales:
bathrooms, bedrooms, beds, review_scores_location,review_scores_value

lets drop na-s */

drop if missing(bathrooms, bedrooms, beds, review_scores_location,review_scores_value)

codebook

* now we can consider this data cleaned so let's save it 

mkdir "clean"

save "clean/airbnb_clean.dta", replace
