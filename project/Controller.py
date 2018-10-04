import pandas as pd

class Controller(object):
	""" Classe de Controller usada para gerenciar e coordenar os acessos as funcoes """
	
	#Criando um dataframe vazio para guardar os documentos
	docummentData = pd.DataFrame(columns=['userId', 'url'])
	#Criando um dataframe vazio para guardar as recomendacoes de urls e seus scores.
	recommendUrls = pd.DataFrame(columns=('url', 'url_recommend', 'score'))

	def send_url(self, documment):
		""" Metodo para armazenar uma url visualizada """
		try:
			self.docummentData =  self.docummentData.append(documment, ignore_index=True)
			print("DataFrame ->" + str(self.docummentData))

		except Exception as e:
			return self.createDataError("ERROR TO INCLUDE NEW URL", "001")

		return {"status": "SUCCESS", "message": "URL INCLUDE WITH SUCCESS"}


	def get_similar_url(self, url):
		#Ordena as urls similares em ordem decrescemte
		result_list = self.recommendUrls[self.recommendUrls.url==url][["url_recommend","score"]].sort_values("score", ascending=[0])
		result_list.columns = ['url', 'score']
		result_list = result_list.head(10)
		return result_list.to_json(orient='records')


	def process_urls_similar(self):
		if not self.recommendUrls.empty:
			#Limpa o dataframe para evitar acumulo de dados processados anteriormente e redundantes
			self.recommendUrls.drop(self.recommendUrls.index, inplace=True)

		try:
			#Recupera a lista das urls unicas
			urlsList=list(set(self.docummentData["url"].tolist()))

			#Compara cada url na lista com outra url da mesma lista
			for urlFirstList in urlsList:
			    
			    #Recupera os usuarios que visitaram essa url
			    urlsUserFirst = self.docummentData.loc[self.docummentData.url == urlFirstList, "userId"].tolist()
			    
			    #Percorre a lista de urls para comparar com as outras urls visitadas
			    for urlSecondList in urlsList:
			        #Ignora a mesma url e compara somente as diferentes
			        if ( urlFirstList != urlSecondList ):
				        #Recupera os usuarios que visitaram essa proxima url
				        urlsUserSecond = self.docummentData.loc[self.docummentData.url == urlSecondList, "userId"].tolist()
				        
				        #Acha o score atraves da divisao do total de usuarios comuns com o total de usuarios que visitaram qualquer uma das urls
				        sameUsersForTwoURLS = len(set(urlsUserFirst).intersection(set(urlsUserSecond)))
				        allUsersForTwoURLS = len(set(urlsUserFirst).union(set(urlsUserSecond)))
				        score = sameUsersForTwoURLS / allUsersForTwoURLS

				        #Adiciona o score para as urls similares
				        self.recommendUrls = self.recommendUrls.append({'url': urlFirstList, 'url_recommend': urlSecondList, 'score': score}, ignore_index=True)				      

		except Exception as e:
			print(str(e))
			return self.createDataError("ERROR TO PROCESS SIMILAR URL", "002")
			        
		return {"status": "SUCCESS", "message": "SUCCESS TO PROCESS SIMILAR URL"}
		

	def createDataError(self, msg, errorCode):
		error_data = {}
		error_data['error_code'] = errorCode
		error_data['description'] = msg

		return error_data
		