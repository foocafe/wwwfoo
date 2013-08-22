/**
 * Removes duplicates in the array 'a'
 * @author Johan Känngård, http://johankanngard.net/
 */
function unique(a) {
	tmp = new Array(0);
	for(i=0;i<a.length;i++){
		if(!contains(tmp, a[i])){
			tmp.length+=1;
			tmp[tmp.length-1]=a[i];
		}
	}
	return tmp;
}

/**
 * Returns true if 's' is contained in the array 'a'
 * @author Johan Känngård, http://johankanngard.net/
 */
function contains(a, e) {
	for(j=0;j<a.length;j++)if(a[j]==e)return true;
	return false;
}



function removeItems(array, item) {
	var i = 0;
	while (i < array.length) {
		if (array[i] == item) {
			array.splice(i, 1);
		} else {
			i++;
		}
	}
	return array;
}


$(document).ready(function () {
	
	// everything hinges on creating a string of class names, 
	// so i'll create a variable to hold that first
	
	var stringOfClassNames = '';
	
	// grab the class name of each list item to build that string
	$('.filterThis > li').each( function (i) {
		var thisClassString = $(this).attr('class');
		stringOfClassNames = stringOfClassNames +' '+ thisClassString
	});
	
	// now i have a space-delimited string of all class names stored
	// in the stringOfClassNames variable.	
	// Trim spaces from the ends of that string:
	stringOfClassNames = jQuery.trim(stringOfClassNames);
	
	// i can't really do anything with it until it's an array, so
	// convert that string to an array.
	var arrayClasses = stringOfClassNames.split(' ');
	
	
	// now for the isolating the filter that is common to all.
	// must do before extracting only the unique classes
	// one way to approach: count the number of times classes occur, and
	// if any occur the same number of times as how many list items i have,
	// assume that class is common to all list items, and remove it from
	// the filter list. duplicate class on same item = problem, but 
	// i'm not thinking about that right now.
	// i've also chosen sort the pre-unique'd array
	// instead of sorting the unique'd array.  i think i have to for the count.
	var arrayClasses = arrayClasses.sort();
	totalNumberOfItemsToFilter = $('.filterThis > li').length;
	
	
	// borrowed from http://stackoverflow.com/questions/348021/counting-results-in-an-array
	// for counting up items.  do i even need this?
	var result = new Object();
	for (var filterClass in arrayClasses) {
		if (result[arrayClasses[filterClass]] === undefined) {
			result[arrayClasses[filterClass]] = 1;
		} else {
			result[arrayClasses[filterClass]]++;
		}
	}
	var resultsToRemoveFromFilters = new Array();
	for (var item in result) {
		if (result[item] == totalNumberOfItemsToFilter) {
			resultsToRemoveFromFilters.push(item);
		}
	}
	
	
	

	// pull out only unique values from that array.  Otherwise
	// i'll end up with duplicate filter checkboxes.
	arrayUniqueClasses = (unique(arrayClasses));


	// and now remove classes that appear in every result from my 'unique
	// classes' array
	//for (x in resultsToRemoveFromFilters) {
	//	arrayUniqueClasses = removeItems(arrayUniqueClasses,resultsToRemoveFromFilters[x]);
	//}
	//$('.filterThis').before('<p><strong>Classes excluded from filters because they are common to all elements:<\/strong> '+resultsToRemoveFromFilters+'<\/p>');



	// we only want to create filters if there are multiple classes. check
	// length of that array to see if it worth going forward.  I need at least
	// two, so my value has to be greater than 1.
	if (arrayUniqueClasses.length > 1) {

		// it must be worth it, because everything else is
		// within the true side of this if statement.	
		// so since we're going to have some filters, 
		// lets give them a place to live
		//$('<ul class="filters"><\/ul>').insertBefore('.filterThis');
		
		// then build the filter checkboxes based on all the class names
		//$.each(arrayUniqueClasses, function() {
		//	$('<li><input class="dynamicFilterInput" type="checkbox" checked="checked" value="'+this+'" id="filterID'+this+'" /><label for="filterID'+this+'">'+this+'<\/label><\/li>').appendTo('ul.filters');
		//});
		
		// lets throw in the 'show all' checkbox for giggles
		//$('<li><input type="checkbox" checked="checked" value="filterAll" id="filterIDall" /><label for="filterIDall">Show all<\/label><\/li>').appendTo('ul.filters');

		// now lets give those filters something to do
		$('.filters input').click( function() {
			var value= $(this).val();
			if ((value == 'filterAll') && ($(this).is(':checked'))) {
				$('.filters input').attr('checked','checked');
				$('.filterThis li').slideDown();
			} else {
				stringValue = '.filterThis > li.'+value;
				stringValueOpposite = '.filterThis > li:not(.'+value+')';
				if ($(this).is(':checked')) {
					classesOfItemToShow = '';
					$(stringValue).slideDown().each( function() {
						classesOfItemToShow = classesOfItemToShow + ' ' + $(this).attr('class');
					});
					// trim spaces, then turn to an array, then
					// exclude non-unique classes
					classesOfItemToShow = jQuery.trim(classesOfItemToShow);
					classesOfItemToShow = classesOfItemToShow.split(' ');
					classesOfItemToShow = (unique(classesOfItemToShow));
					if (classesOfItemToShow.length > 1) {
						$.each(classesOfItemToShow, function() {
							$('.filters input[value='+this+']').attr('checked','true');
						});	
					}
					if ($('.dynamicFilterInput').not(':checked').length == 0) {
						$('#filterIDall').attr('checked','true');
					};
				} else {
					// all my new stuff goes here to tackle that 'webdev'
					// and 'resources' class issue.
					OtherClassesAssociatedWithTheItemToBeRemoved = '';
					Oca = OtherClassesAssociatedWithTheItemToBeRemoved;
					$(stringValue).each(function(i) {
						Oca = Oca + ' ' + $(this).attr('class');
					});
					
					// trim spaces, then turn to an array, then
					// exclude non-unique classes
					Oca = jQuery.trim(Oca);
					Oca = Oca.split(' ');
					Oca = (unique(Oca));
					if (Oca.length > 1) {
						$.each(Oca, function() {
							classToCompare = this; 
							if (!($('.'+classToCompare).is(stringValueOpposite))) {
								// uncheck the checkbox that classToCompare represents
								$('.filters input[value='+classToCompare+']').removeAttr('checked');
							}
						});	
					}
					$(stringValue).slideUp();
					$('.filters #filterIDall').removeAttr('checked');
				}
			}
		});
	}
});