cd "C:\Users\Pakozdi_Benedek\Desktop\Coding for economics\assignment\Stata"

do cleaning.do

cd "C:\Users\Pakozdi_Benedek\Desktop\Coding for economics\assignment\Stata"

mkdir "Stata_output"

** lets create a few new descriptive variable:

generate price_per_person = price/accommodates

/* generate host qualitz index
- first we need to standardize the host related variables and then take the mean of the standardized variables */ 

foreach var in host_response_rate host_is_superhost host_identity_verified {
    egen z_`var' = std(`var')
}

egen host_quality_index = rowmean(z_host_response_rate z_host_is_superhost z_host_identity_verified)

drop z_host_identity_verified z_host_is_superhost z_host_response_rate

** now lets run the analysises 

summarize price bedrooms bathrooms host_quality_index number_of_reviews 

/* statistics about room charachteristics */
tabstat price, by(room_type) statistics(mean sd median)
tabstat price, by(instant_bookable) statistics(mean sd)
tabstat price, by(cancellation_policy) statistics(mean sd)

/*statistics about host charachteristics*/
tabstat price, by(host_is_superhost) statistics(mean sd)
tabstat price, by(host_identity_verified) statistics(mean sd)
tabstat price, by(host_has_profile_pic) statistics(mean sd)

/*superhost doen't mean a lot but the profil picture and the verified identity showes a 10 dollar mean difference*/


** correlations ** 

pwcorr price host_quality_index

pwcorr price is_location_exact accommodates bathrooms bedrooms minimum_nights

pwcorr price host_quality_index number_of_reviews review_scores_location review_scores_value

**** graphs *****

/*histogram of prices*/

histogram price, width(20) start(0) percent title("Distribution of Airbnb Prices")
graph export "Stata_output/price histogram.pdf", replace

histogram price_per_person, width(20) start(0) percent title("Distribution of Airbnb Prices Per Accommodates")
graph export "Stata_output/price_per_person histogram.pdf", replace

/*graphs about room charachteristics*/

graph bar (mean) price, over(room_type) title("Average Price by Cancellation Policy")
graph export "Stata_output/room_type graph.pdf", replace

/*graphs about host charachteristics*/

twoway (scatter price host_quality_index) (lfit price host_quality_index)
graph export "Stata_output/price - hostquality.pdf", replace



histogram host_quality_index, percent title("Distribution of host quality")
graph export "Stata_output/host quality distribution.pdf", replace
