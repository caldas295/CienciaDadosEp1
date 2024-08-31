import scrapy

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
    domain = "https://pokemondb.net/"

    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            yield response.follow(self.domain + link, self.parse_pokemon)

    def parse_pokemon(self, response):
        # Extraindo URL da página atual
        url_pagina = response.url

        # Extraindo evoluções
        proximas_evolucoes = []
        evolucoes = response.css('.infocard-list-evo .infocard')
        for evolucao in evolucoes:
            evolucao_nome = evolucao.css('a.ent-name::text').get()
            evolucao_numero = evolucao.css('.text-muted::text').get()  # Seletor atualizado para capturar o número
            evolucao_url = response.urljoin(evolucao.css('a.ent-name::attr(href)').get())
            if evolucao_nome and evolucao_numero:  # Verifica se ambos os dados existem
                proximas_evolucoes.append({
                    'numero': evolucao_numero.strip(),  # Remove espaços extras, se houver
                    'nome': evolucao_nome,
                    'url': evolucao_url
                })

        # Extraindo habilidades
        habilidades = []
        habilidades_section = response.css('.vitals-table tr:contains("Abilities") td a')
        for habilidade in habilidades_section:
            habilidade_nome = habilidade.css('::text').get()
            habilidade_url = response.urljoin(habilidade.css('::attr(href)').get())
            habilidades.append({
                'nome': habilidade_nome,
                'url': habilidade_url
            })

        yield {
            'pokemon_id': response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
            'pokemon_proximas_evolucoes': proximas_evolucoes,
            'pokemon_name': response.css('#main > h1::text').get(),
            'pokemon_altura': response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get(),
            'pokemon_peso': response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get(),
            'pokemon_tipos': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a::text').getall(),
            'pokemon_habilidades': habilidades,
            'url_pagina': url_pagina
        }
