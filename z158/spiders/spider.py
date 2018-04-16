import scrapy
from z158.items import Z158Item
from scrapy import Request
from scrapy import FormRequest
class z158(scrapy.Spider):
	name='z158'
	start_urls=['http://www.z158.cn/users/login.asp',]
	USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
	Referer = 'http://www.z158.cn/'
	headers={'User-Agent':USER_AGENT}
	def parse(self,response):
		formdate = {
		'username' :'',
		'password' : ''
		}
		return [FormRequest.from_response(response,formdata=formdate,headers=self.headers,callback=self.after_login)]
	def after_login(self,response):
		lnk='http://www.z158.cn'
		#print('login success')
		return Request(lnk,callback=self.parse_list)
	def parse_list(self,response):
		#列表页面解析，获取详细分类的链接
		listinfos = response.xpath('//div[@class="clearfix sub-det"]/div/h3/a')
		'''
		for listinfo in listinfos:
			#分类链接
			listurl = listinfo.xpath('@href').extract()[0]
			
			yield Request(listurl,callback=self.new_list_page)
		'''
		listurl='http://www.z158.cn/jiangzuo/list_1_94.html'
		yield Request(listurl,callback=self.new_list_page,meta={'url':listurl})
	def new_list_page(self,response):
		try:
			page_num = response.xpath('//div[@class="page cf"]/code/a/text()').extract()[-2]
		except Exception as e:
			pass
		for page in range(1,int(page_num)):
                        url_split=response.meta['url'].split('_')
                        url = url_split[0]+'_'+str(page)+'_'+url_split[2]
                        yield Request(url,callback=self.new_list)


	def new_list(self,response):
		#列表详情页面解析，获取内容页面的url
		infos = response.xpath('//div[@class="zl_r_list cf"]/div[@class="zl_list_con"]/div[@class="top"]/h5/a')	
		for info in infos:
			#内容页面的url
			url = info.xpath('@href').extract()[0]
			yield Request(url,callback=self.last_info)
	def last_info(self,response):
		#资源内容页面解析,获取资源内容的url		
		url = response.xpath('//div[@class="zl_cz"]/a[1]/@href').extract_first()
		url = response.urljoin(url)
		name = response.xpath('//h1/text()').extract_first()
		yield Request(url,callback=self.srcurl,meta={'name':name})
	def srcurl(self,response):
		#资源下载url解析
		srcurl = response.xpath('//div[@class="i_login"]/a/@href').extract()[0]
		if not srcurl=='javascript:':
			full_srcurl = response.urljoin(srcurl)
			Referer = response.url		
			headers={'User-Agent':self.USER_AGENT,'Referer':Referer}
			yield Request(full_srcurl,headers=headers,callback=self.src,meta=response.meta)
		else:
			print('unuseful src:',response.url)	
	def src(self,response):
		item = Z158Item()
		src = response.xpath('//div[@class="downarea"]/a[2]/@href').extract()[0]
		if src:
			item['src'] = src
			item['name'] = response.meta['name']
			return item
		return None

