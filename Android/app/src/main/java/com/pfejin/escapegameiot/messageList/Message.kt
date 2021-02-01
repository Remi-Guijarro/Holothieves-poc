package com.pfejin.escapegameiot.messageList

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

enum class MessageAuthor {
    PLAYER,
    GAME_MASTER
}

@Serializable
data class Message(
    @SerialName("author")
    val author: MessageAuthor,
    @SerialName("text")
    val text : String
)