from typing import Any, Dict, List

import hikari
from lightbulb import BotApp
from datetime import datetime
from API import search


def scrape(params: Dict[str, str]) -> List:
    """
    Scrape les items et les filtre par nouveaux resultats

    Args:
        params (Dict[str, str]): Elements de la database

    Returns:
        List: liste des nouveaux items
    """
    response = search(params['url'], {'per_page': 20})

    # Suprrime les items sponsos
    items = [item for item in response['items'] if item['promoted'] == False]

    # Passe le null
    if not len(items):
        return []

    # Ignore les items à la premiere sync
    if params['synced'] == False:
        return [items[0]]

    # Filtre de date
    items = [item for item in items if item['photo']
             ['high_resolution']['timestamp'] > params['last_sync']]

    return items


def generate_embed(item: Any, sub_id: int) -> hikari.Embed:
    """
    Genere un embed avec les details des items

    Args:
        item (Any): Item scrapé
        sub_id (int): Id de l'abo

    Returns:
        hikari.Embed: Embeb generé
    """
    embed = hikari.Embed()
    embed.title = item['title'] or "Unknown"
    embed.url = item['url'] or "Unknown"
    embed.set_image(item['photo']['url'] or "Unknown")
    embed.color = hikari.Color(0x09b1ba)
    embed.add_field('Price', str(item['price']+'€') or "-1" + '€', inline=True)
    embed.add_field('Size', item['size_title'] or "-1", inline=True)

    date = datetime.utcfromtimestamp(
        int(item['photo']['high_resolution']['timestamp'])).strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(
        f'Published on {date or "unknown"} • Subscription #{str(sub_id)}')
    embed.set_author(name='Posted by ' + item['user']['login'] or "unknown",
                     url=item['user']['profile_url'] or "unknown")

    return embed


def generate_row(bot: BotApp, item: Any, link: str) -> Any:
    """
    Generate a component row with a button
    to redirect user on Vinted

    Args:
        bot (BotApp): Bot instance
        item (Any): Item
        link (str): Original search link

    Returns:
        Any: Generated row
    """
    row = bot.rest.build_action_row()

    if item['url']:
        (
            row.add_button(hikari.ButtonStyle.LINK, item['url'])
            .set_label('View article')
            .set_emoji('🛍')
            .add_to_container()
        )

    (
        row.add_button(hikari.ButtonStyle.LINK, link)
        .set_label('Search list')
        .set_emoji('🔍')
        .add_to_container()
    )

    (
        row.add_button(
            hikari.ButtonStyle.LINK,
            'https://www.vinted.fr/transaction/buy/new?source_screen=item&transaction%5Bitem_id%5D=' +
            str(item['id'])
        )
        .set_label('Buy')
        .set_emoji('💵')
        .add_to_container()
    )

    return row


