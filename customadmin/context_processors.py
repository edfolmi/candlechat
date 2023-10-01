from chat.models import Block

def blocks_chart(request):
    blocks_in_chart = Block.objects.all()

    blockchart = []

    for block in blocks_in_chart:
        name = block.name
        online = block.online.count()

        blockchart.append({'name': name, 'online': online})

    return {'blockchart': blockchart}
