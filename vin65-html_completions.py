import sublime, sublime_plugin
import re

def match(rex, str):
    m = rex.match(str)
    if m:
        return m.group(0)
    else:
        return None

# This responds to on_query_completions, but conceptually it's expanding
# expressions, rather than completing words.
#
# It expands these simple expressions:
# tag.class
# tag#id
class HtmlCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within HTML
        if not view.match_selector(locations[0],
                "text.html - source - meta.tag, punctuation.definition.tag.begin"):
            return []

        # Get the contents of each line, from the beginning of the line to
        # each point
        lines = [view.substr(sublime.Region(view.line(l).a, l))
            for l in locations]

        # Reverse the contents of each line, to simulate having the regex
        # match backwards
        lines = [l[::-1] for l in lines]

        # Check the first location looks like an expression
        rex = re.compile("([\w-]+)([.#])(\w+)")
        expr = match(rex, lines[0])
        if not expr:
            return []

        # Ensure that all other lines have identical expressions
        for i in xrange(1, len(lines)):
            ex = match(rex, lines[i])
            if ex != expr:
                return []

        # Return the completions
        arg, op, tag = rex.match(expr).groups()

        arg = arg[::-1]
        tag = tag[::-1]
        expr = expr[::-1]

        if op == '.':
            snippet = "<{0} class=\"{1}\">$1</{0}>$0".format(tag, arg)
        else:
            snippet = "<{0} id=\"{1}\">$1</{0}>$0".format(tag, arg)

        return [(expr, snippet)]


# Provide completions that match just after typing an opening angle bracket
class TagCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within HTML
        if not view.match_selector(locations[0],
                "text.html - source"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return []

        return ([
            ("v65:ageGate\tTag", "v65:ageGate></v65:ageGate>"),
            ("v65:birthDateValidation\tTag", "v65:birthDateValidation></v65:birthDateValidation>"),
            ("v65:blogArchives\tTag", "v65:blogArchives></v65:blogArchives>"),
            ("v65:blogAuthors\tTag", "v65:blogAuthors></v65:blogAuthors>"),
            ("v65:blogCategories\tTag", "v65:blogCategories></v65:blogCategories>"),
            ("v65:blogRecentPosts\tTag", "v65:blogRecentPosts></v65:blogRecentPosts>"),
            ("v65:blogSearch\tTag", "v65:blogSearch></v65:blogSearch>"),
            ("v65:blogSubscribeByRSS\tTag", "v65:blogSubscribeByRSS></v65:blogSubscribeByRSS>"),
            ("v65:blogWidget\tTag", "v65:blogWidget></v65:blogWidget>"),
            ("v65:breadCrumbs\tTag", "v65:breadCrumbs${1: delimiter=\"$2\"}></v65:breadCrumbs>$0"),
            ("v65:contentBlock\tTag", "v65:contentBlock group=\"$1\"></v65:contentBlock>$0"),
            ("v65:contentSearch\tTag", "v65:contentSearch></v65:contentSearch>"),
            ("v65:copyright\tTag", "v65:copyright></v65:copyright>"),
            ("v65:css\tTag", "v65:css files=\"${1:/assets/css/screen.min.css}\"></v65:css>$0"),
            ("v65:eventToday\tTag", "v65:eventToday></v65:eventToday>"),
            ("v65:eventUpcoming\tTag", "v65:eventUpcoming></v65:eventUpcoming>"),
            ("v65:js\tTag", "v65:js files=\"/assets/js/${1:scripts}.js$2\"></v65:js>$0"),
            ("v65:layoutFooterNav\tTag", "v65:layoutFooterNav></v65:layoutFooterNav>"),
            ("v65:layoutHeaderNav\tTag", "v65:layoutHeaderNav ${1: depth=\"${2:2}\"}></v65:layoutHeaderNav>"),
            ("v65:layoutLeftNav\tTag", "v65:layoutLeftNav ${1: startDepth=\"${2:2}\"></v65:layoutLeftNav>$0"),
            ("v65:layoutSubMenu\tTag", "v65:layoutSubMenu></v65:layoutSubMenu>"),
            ("v65:leftNavSectionTitle\tTag", "v65:leftNavSectionTitle></v65:leftNavSectionTitle>"),
            ("v65:login\tTag", "v65:login${1: delimiter=\"$2\"}></v65:login>$0"),
            ("v65:mainContent\tTag", "v65:mainContent></v65:mainContent>"),
            ("v65:metaTags\tTag", "v65:metaTags></v65:metaTags>"),
            ("v65:modalCart\tTag", "v65:modalCart></v65:modalCart>"),
            ("v65:navBrand\tTag", "v65:navBrand></v65:navBrand>"),
            ("v65:navPrice\tTag", "v65:navPrice></v65:navPrice>"),
            ("v65:navRegionAppellation\tTag", "v65:navRegionAppellation></v65:navRegionAppellation>"),
            ("v65:navVintage\tTag", "v65:navVintage></v65:navVintage>"),
            ("v65:navtypeVarietal\tTag", "v65:navtypeVarietal></v65:navtypeVarietal>"),
            ("v65:pageTitle\tTag", "v65:pageTitle></v65:pageTitle>"),
            ("v65:pods\tTag", "v65:pods location=\"$1\" type=\"${2:title/image/description}${2/(t$)|(i$)|(d$)|.*/?1:itle:?2:mage:?3:escription/},$3\"></v65:pods>$0"),
            ("v65:product:actionMessage\tTag", "v65:product:actionMessage></v65:product:actionMessage>"),
            ("v65:product:addToCart\tTag", "v65:product:addToCart></v65:product:addToCart>"),
            ("v65:product:availability\tTag", "v65:product:availability></v65:product:availability>"),
            ("v65:product:brand\tTag", "v65:product:brand></v65:product:brand>"),
            ("v65:product:countdown\tTag", "v65:product:countdown></v65:product:countdown>"),
            ("v65:product:customAttribute\tTag", "v65:product:customAttribute></v65:product:customAttribute>"),
            ("v65:product:description\tTag", "v65:product:description></v65:product:description>"),
            ("v65:product:drilldownLink\tTag", "v65:product:drilldownLink></v65:product:drilldownLink>"),
            ("v65:product:group\tTag", "v65:product:group></v65:product:group>"),
            ("v65:product:inCompliantStateMessage\tTag", "v65:product:inCompliantStateMessage></v65:product:inCompliantStateMessage>"),
            ("v65:product:inventoryMessage\tTag", "v65:product:inventoryMessage></v65:product:inventoryMessage>"),
            ("v65:product:media\tTag", "v65:product:media></v65:product:media>"),
            ("v65:product:pagination\tTag", "v65:product:pagination></v65:product:pagination>"),
            ("v65:product:photo\tTag", "v65:product:photo></v65:product:photo>"),
            ("v65:product:photos\tTag", "v65:product:photos></v65:product:photos>"),
            ("v65:product:relatedProducts\tTag", "v65:product:relatedProducts></v65:product:relatedProducts>"),
            ("v65:product:reviewStats\tTag", "v65:product:reviewStats></v65:product:reviewStats>"),
            ("v65:product:reviews\tTag", "v65:product:reviews></v65:product:reviews>"),
            ("v65:product:shipDate\tTag", "v65:product:shipDate></v65:product:shipDate>"),
            ("v65:product:sku\tTag", "v65:product:sku></v65:product:sku>"),
            ("v65:product:socialBar\tTag", "v65:product:socialBar></v65:product:socialBar>"),
            ("v65:product:sortby\tTag", "v65:product:sortby></v65:product:sortby>"),
            ("v65:product:subtitle\tTag", "v65:product:subtitle></v65:product:subtitle>"),
            ("v65:product:teaser\tTag", "v65:product:teaser></v65:product:teaser>"),
            ("v65:product:title\tTag", "v65:product:title></v65:product:title>"),
            ("v65:productFilter\tTag", "v65:productFilter></v65:productFilter>"),
            ("v65:productSearch\tTag", "v65:productSearch></v65:productSearch>"),
            ("v65:rssFeed\tTag", "v65:rssFeed></v65:rssFeed>"),
            ("v65:shippingWidget\tTag", "v65:shippingWidget></v65:shippingWidget>"),
            ("v65:siteLogin\tTag", "v65:siteLogin></v65:siteLogin>"),
            ("v65:spirit:country\tTag", "v65:spirit:country></v65:spirit:country>"),
            ("v65:spirit:region\tTag", "v65:spirit:region></v65:spirit:region>"),
            ("v65:spirit:type\tTag", "v65:spirit:type></v65:spirit:type>"),
            ("v65:stateProfile:complianceAdvisory\tTag", "v65:stateProfile:complianceAdvisory></v65:stateProfile:complianceAdvisory>"),
            ("v65:subscribe\tTag", "v65:subscribe contactType=\"${1:Newsletter}\"></v65:subscribe>$0"),
            ("v65:suggestedProducts\tTag", "v65:suggestedProducts dataType=\"${1:Both/Purchase/Product}${1/(B$)|(Pu$)|(Pr$)|.*/?1:oth:?2:rchase:?3:oduct/i}\" priceRange=\"${2:5}\" maxRows=\"${3:5}\" rank=\"{price=$4,varietal=$5,region=$6}\" layout=\"$7\" title=\"$8\"></v65:suggestedProducts>$0"),
            ("v65:twitterFeed\tTag", "v65:twitterFeed searchQuery=\"$1\"></v65:twitterFeed>$0"),
            ("v65:vin65Accolade\tTag", "v65:vin65Accolade></v65:vin65Accolade>"),
            ("v65:websiteName\tTag", "v65:websiteName></v65:websiteName>"),
            ("v65:wine:acid\tTag", "v65:wine:acid></v65:wine:acid>"),
            ("v65:wine:aging\tTag", "v65:wine:aging></v65:wine:aging>"),
            ("v65:wine:alcohol\tTag", "v65:wine:alcohol></v65:wine:alcohol>"),
            ("v65:wine:appellation\tTag", "v65:wine:appellation></v65:wine:appellation>"),
            ("v65:wine:awards\tTag", "v65:wine:awards></v65:wine:awards>"),
            ("v65:wine:bottleSize\tTag", "v65:wine:bottleSize></v65:wine:bottleSize>"),
            ("v65:wine:bottlingDate\tTag", "v65:wine:bottlingDate></v65:wine:bottlingDate>"),
            ("v65:wine:fermentation\tTag", "v65:wine:fermentation></v65:wine:fermentation>"),
            ("v65:wine:foodPairingNotes\tTag", "v65:wine:foodPairingNotes></v65:wine:foodPairingNotes>"),
            ("v65:wine:harvestDate\tTag", "v65:wine:harvestDate></v65:wine:harvestDate>"),
            ("v65:wine:otherNotes\tTag", "v65:wine:otherNotes></v65:wine:otherNotes>"),
            ("v65:wine:ph\tTag", "v65:wine:ph></v65:wine:ph>"),
            ("v65:wine:production\tTag", "v65:wine:production></v65:wine:production>"),
            ("v65:wine:productionNotes\tTag", "v65:wine:productionNotes></v65:wine:productionNotes>"),
            ("v65:wine:professionalReviews\tTag", "v65:wine:professionalReviews></v65:wine:professionalReviews>"),
            ("v65:wine:profile\tTag", "v65:wine:profile></v65:wine:profile>"),
            ("v65:wine:ratings\tTag", "v65:wine:ratings></v65:wine:ratings>"),
            ("v65:wine:region\tTag", "v65:wine:region></v65:wine:region>"),
            ("v65:wine:residualSugar\tTag", "v65:wine:residualSugar></v65:wine:residualSugar>"),
            ("v65:wine:specs\tTag", "v65:wine:specs></v65:wine:specs>"),
            ("v65:wine:sugar\tTag", "v65:wine:sugar></v65:wine:sugar>"),
            ("v65:wine:tannin\tTag", "v65:wine:tannin></v65:wine:tannin>"),
            ("v65:wine:tastingNotes\tTag", "v65:wine:tastingNotes></v65:wine:tastingNotes>"),
            ("v65:wine:type\tTag", "v65:wine:type></v65:wine:type>"),
            ("v65:wine:varietal\tTag", "v65:wine:varietal></v65:wine:varietal>"),
            ("v65:wine:vineyardDesignation\tTag", "v65:wine:vineyardDesignation></v65:wine:vineyardDesignation>"),
            ("v65:wine:vineyardNotes\tTag", "v65:wine:vineyardNotes></v65:wine:vineyardNotes>"),
            ("v65:wine:vintage:notes\tTag", "v65:wine:vintage:notes></v65:wine:vintage:notes>"),
            ("v65:wine:vintageNotes\tTag", "v65:wine:vintageNotes></v65:wine:vintageNotes>"),

        ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
