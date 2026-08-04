from sqlalchemy import select
from aiogram.utils.text_decorations import html_decoration

from app.db.models import Dialog as DialogModel

from app.config import ADMIN_CHAT


class Dialog:
    def __init__(self,session,bot,id:int = None,peer:int|str = None,name=None):
        self.session = session
        self.bot = bot

        self.name = name
        self.admin_chat = ADMIN_CHAT

        self.id = id
        self.peer = peer


    async def __ainit__(self):
        match self.id,self.peer:
            case int(id),None:
                self.peer = await self.__get_dialog_peer(id)
                if not self.peer:
                    return None

            case None,int(peer):
                self.id = await self.__get_dialog_id(peer)

            case None,str(peer):
                chat = await self.bot.get_chat(peer)
                if chat.type == 'private':
                    self.name = f"{chat.first_name} {chat.last_name or ''}"
                else:
                    self.name = chat.title
                self.id = await self.__get_dialog_id(chat.id)
                self.peer = chat.id

            case _:
                raise ValueError('id=None,peer=None')

        if not self.id:
            self.id = await self.__create_dialog()

        return self


    def __await__(self):
        return self.__ainit__().__await__()


    async def __create_dialog(self) -> int:
        topic = await self.bot.create_forum_topic(
            chat_id=self.admin_chat,
            name=self.name
        )

        dialog = DialogModel(
            id=topic.message_thread_id,
            peer_id=self.peer,
        )

        self.session.add(dialog)
        await self.session.commit()

        safe_name = html_decoration.quote(self.name)
        link = f'<a href="tg://user?id={self.peer}">{safe_name}</a>' if self.peer > 0 else None

        await self.bot.send_message(
            self.admin_chat,
            f"id: {self.peer}\n"
            f"name: {link or safe_name}\n\n"
            "Діалог розпочато!",
            message_thread_id=dialog.id,
        )

        return dialog.id


    async def __get_dialog_id(self,peer_id) -> int:
        stmt = select(DialogModel.id).where(
            DialogModel.peer_id == peer_id,
        )
        return await self.session.scalar(stmt)


    async def __get_dialog_peer(self,dialog_id) -> int:
        stmt = select(DialogModel.peer_id).where(
            DialogModel.id == dialog_id,
        )
        return await self.session.scalar(stmt)
