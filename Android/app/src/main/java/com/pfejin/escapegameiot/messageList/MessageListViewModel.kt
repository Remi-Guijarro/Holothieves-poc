package com.pfejin.escapegameiot.messageList

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.random.Random

class MessageListViewModel : ViewModel() {
    private val _messagesList = MutableLiveData<List<Message>>()
    public val messagesList: LiveData<List<Message>> = _messagesList

    private var index: Int = 0
    private var hintIndex: Int = 0
    private val delayMessage: Long = 700

    private val messageCount by lazy {
        finishedGMList.size
    }

    private val questionsPlayerList = listOf<Message>(
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Nous avons besoin d'aide.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Nous ne savons pas quoi faire.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Pouvez-vous nous donner plus d'indice.
                    """.trimIndent()
            )
    )

    private val finishedPlayerList = listOf<Message>(
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Nous avons réussi.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.PLAYER,
                    """
                    L'énigme est résolue.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Enigme réussie sans problème.
                    """.trimIndent()
            ),
    )

    private val unfinishedPlayerList = listOf<Message>(
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Je me suis trompé, nous n'avons pas fini la tâche précédente.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Pouvez-vous nous réexpliquer la tâche précédente ?
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.PLAYER,
                    """
                    Pouvez-vous nous récapituler la tâche précédente ?
                    """.trimIndent()
            ),
    )

    private val firstHintGMList = listOf<Message>(
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    N’hésitez pas à vous aider du matériel de haute technologie à votre disposition et d’explorer l’ensemble de la pièce.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Une fois connecté à la borne wi-fi un bouton est apparu dans le casque pour hacker un drone.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Un indice a du apparaître quelque part.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Il n’y a pas un digicode dans la pièce ?
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Avec le casque, vous devriez apercevoir l’élément à mettre en état de nuire.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Il faut procéder au redémarrage du système de lecteur de badge.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Aidez vous du casque pour télécharger les données.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Vous avez gagné. Je n'ai pas d'autres indices à vous donner.
                    """.trimIndent()
            ),
    )

    private val secondHintGMList = listOf<Message>(
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Mettez le casque et trouvez la borne wifi en vous déplaçant dans la pièce.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Vous devriez pouvoir le faire bouger à l’aide d’un joystick...
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Il n’y a pas un papier dans la pièce avec des chiffres et des couleurs ?
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Je ne peux pas plus vous aider.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Pour mettre en état de nuire cet élément, mettez le dans l’eau.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Il faut appuyer sur deux boutons en même temps pour réinitialiser le système.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Je ne peux pas plus vous aider.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Vous avez gagné. Je n'ai pas d'autres indices à vous donner.
                    """.trimIndent()
            ),
    )

    private val finishedGMList = listOf<Message>(
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Ici votre patron, bien joué vous êtes maintenant entré au sein de la banque sans vous faire repérer. Cependant, vous disposez de seulement 20 minutes avant que le garde de surveillance ne revienne de sa pause, alors vous n’avez pas une seconde à perdre ! 
                    Vous devez tout d’abord vous connecter au réseau wifi.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Bien joué ! Vous devriez réussir à hacker un drone.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Super ! Vous devriez réussir à trouver un code.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Vous devriez pouvoir mettre le code quelque part...
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Attention vous avez déclenché une alarme ! Il faut que vous trouviez un moyen de l’arrêter rapidement pour éviter de vous faire repérer.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Vous devez maintenant désactiver le pare-feu pour télécharger les données.
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Parfait maintenant il vous reste juste à télécharger les données !
                    """.trimIndent()
            ),
            Message(
                    MessageAuthor.GAME_MASTER,
                    """
                    Bravo vous avez réussi !
                    """.trimIndent()
            ),
    )

    fun receiveHint() {
        viewModelScope.launch {
            delay(delayMessage)
            val editableList = _messagesList.value.orEmpty().toMutableList()
            when (hintIndex) {
                0 -> editableList.add(firstHintGMList[index])
                1 -> editableList.add(secondHintGMList[index])
                else -> editableList.add(
                        Message(
                                MessageAuthor.GAME_MASTER,
                                """
                                Je ne peux pas plus vous aider.
                                """.trimIndent()
                        )
                    )
            }

            ++hintIndex
            _messagesList.value = editableList
        }
    }

    fun startGM() {
        viewModelScope.launch {
            delay(delayMessage)
            val editableList = _messagesList.value.orEmpty().toMutableList()
            editableList.add(finishedGMList[0])
            _messagesList.value = editableList
        }
    }

    fun receiveFinished() {
        viewModelScope.launch {
            delay(delayMessage)
            if (index < messageCount - 1) {
                ++index
            }
            hintIndex = 0
            val editableList = _messagesList.value.orEmpty().toMutableList()
            editableList.add(finishedGMList[index])
            _messagesList.value = editableList
        }
    }

    fun sendFinished() {
        viewModelScope.launch {
            val editableList = _messagesList.value.orEmpty().toMutableList()
            editableList.add(finishedPlayerList[Random.nextInt(0, 2)])
            _messagesList.value = editableList
        }
    }

    fun sendUnfinished() {
        viewModelScope.launch {
            val editableList = _messagesList.value.orEmpty().toMutableList()
            editableList.add(unfinishedPlayerList[Random.nextInt(0, 2)])
            if (index > 0) {
                --index
            }
            hintIndex = 0
            _messagesList.value = editableList
        }
    }

    fun sendQuestion() {
        viewModelScope.launch {
            val editableList = _messagesList.value.orEmpty().toMutableList()
            editableList.add(questionsPlayerList[Random.nextInt(0, 2)])
            _messagesList.value = editableList
        }
    }
}