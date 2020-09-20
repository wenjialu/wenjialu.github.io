/**
 * 
 * Meta Maker Helper
 *
 * Use instead of Hexo's built-in %- open_graph() %> helper.
 *
 * Recommended Syntax:
 *   <%- meta_maker() %>
 *
 *	Option			Description					Default
 *
 *	title			Page title					page.title 
 *	title_divider	Divider symbol for title	" | "
 *	type			Page type					website
 *	url				Page URL					page URL
 *	image			Page cover					og-image.jpg
 *	site_name		Site name					config.title
 *	description		Page description			First 200 characters
 *	twitter_card	Twitter card type			summary
 *	twitter_creator	Twitter creator handle
 *	twitter_site	Twitter site handle
 *	google_plus		Google+ profile ID
 *	fb_admins		Facebook admin ID
 *	fb_app_id		Facebook app ID
 *	fb_personal_url	URL to personal Facebook page of author
 *
**/

'use strict';

var urlFn = require('url');
var moment = require('moment');
var util = require('hexo-util');
var htmlTag = util.htmlTag;
var stripHTML = util.stripHTML;
var escapeHTML = util.escapeHTML;
var cheerio;

function meta(name, content, escape) {
  if (escape !== false && typeof content === 'string') {
    content = escapeHTML(content);
  }

  return "\t" + htmlTag('meta', {
    name: name,
    content: content
  }) + '\n';
}

function og(name, content, escape) {
  if (escape !== false && typeof content === 'string') {
    content = escapeHTML(content);
  }

  return "\t" + htmlTag('meta', {
    property: name,
    content: content
  }) + '\n';
}

function metaMakerHelper(options) {
  options = options || {};

  if (!cheerio) cheerio = require('cheerio');

  var page = this.page;
  var config = this.config;
  var theme = this.theme;
  var content = page.content;
  var images = page.photos || theme.og_image_url;
  var description = options.description || page.description || page.excerpt || content || config.description;
  var keywords = page.keywords || (page.tags && page.tags.length ? page.tags : undefined) || config.keywords;
  var type = options.type || (this.is_post() ? 'article' : 'website');
  var url = options.url || this.url.slice(0, -10);
  var siteName = options.site_name || config.title;
  var twitterCard = options.twitter_card || 'summary';
  var updated = options.updated !== false ? (options.updated || page.updated) : false;
  var language = options.language || page.lang || page.language || config.language;
  var result = '';

  if (!Array.isArray(images)) images = [images];

  if (description) {
    description = stripHTML(description).substring(0, 200)
      .trim() // Remove prefixing/trailing spaces
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;')
      .replace(/\n/g, ' '); // Replace new lines by spaces
  }

  if (!images.length && content) {
    images = images.slice();

    var $ = cheerio.load(content);

    $('img').each(function() {
      var src = $(this).attr('src');
      if (src) images.push(src);
    });
  }

  result += meta('author', config.author, false);
  
  result += "\t" + htmlTag('link', {rel: 'canonical', href: url}) + '\n';
  if (description) {
    result += meta('description', description, false);
  }

  if (keywords) {
    if (typeof keywords === 'string') {
      result += meta('keywords', keywords);
    } else if (keywords.length) {
      result += meta('keywords', keywords.map(function(tag) {
        return tag.name ? tag.name : tag;
      }).filter(function(keyword) {
        return !!keyword;
      }).join());
    }
  }
  
  var titleDivider = options.title_divider || theme.title_divider || " | ";
  
  if (page.title){
	  var title = page.title + titleDivider + config.title;
  }
  else {
	  var title = options.title || config.title;
  }

  result += og('og:type', type);
  result += og('og:title', title);
  result += og('og:url', url, false);
  result += og('og:site_name', siteName);
  
  if (type == 'article'){
	result += og('article:published_time', page.date.toISOString());
	if (theme.fb_page_id){
		result += og('article:publisher', 'https://www.facebook.com/' + theme.fb_page_id, false);
		result += og('article:author', 'https://www.facebook.com/' + theme.fb_personal_id, false);
	}
  }
  
  if (description) {
    result += og('og:description', description, false);
  }

  if (language) {
	if (language == 'default'){
		language = 'en_US';
	}
    result += og('og:locale', language, false);
  }

  images = images.map(function(path) {
    if (!urlFn.parse(path).host) {
      // resolve `path`'s absolute path relative to current page's url
      // `path` can be both absolute (starts with `/`) or relative.
      return urlFn.resolve(url || config.url, path);
    }

    return path;
  });
  
  if (images.length) {
	  	  result += "\t" + htmlTag('meta', {property: 'og:image', content: images[0] + "?" + moment.now()}) + '\n';
  }
  else {
	  result += "\t" + htmlTag('meta', {property: 'og:image', content: theme.og_image_url + "?" + moment.now()}) + '\n';
	}

  if (updated) {
    if ((moment.isMoment(updated) || moment.isDate(updated)) && !isNaN(updated.valueOf())) {
	  if (type == "article" && moment.duration(updated.diff(page.date)).asMinutes() > 1 ){
      	result += og('og:updated_time', updated.toISOString());
	  	if (type == "article"){
      		result += og('article:modified_time', updated.toISOString());
      	}
      }
    }
  }

  result += meta('twitter:card', twitterCard);
  result += meta('twitter:title', title);
  if (description) {
    result += meta('twitter:description', description, false);
  }

  if (images.length) {
    result += "\t" + htmlTag('meta', {name: 'twitter:image', content: images[0] + "?" + moment.now()}) + '\n';
  }
  
  else {
	  result += "\t" + htmlTag('meta', {name: 'twitter:image', content: theme.og_image_url + "?" + moment.now()}) + '\n';
  }

  if (theme.twitter_creator) {
    result += meta('twitter:creator', theme.twitter_creator);
  }

  if (theme.twitter_site) {
    result += meta('twitter:site', theme.twitter_site, false);
  }

  if (theme.google_plus) {
    result += "\t" + htmlTag('link', {rel: 'publisher', href: "https://plus.google.com/"+theme.google_plus}) + '\n';
  }

  if (theme.fb_admins) {
    result += og('fb:admins', theme.fb_admins);
  }

  if (theme.fb_app_id) {
    result += og('fb:app_id', theme.fb_app_id);
  }

  return result.trim();
}

hexo.extend.helper.register('meta_maker', metaMakerHelper);
