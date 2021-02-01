package com.pfejin.escapegameiot.messageList

import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.text.style.BackgroundColorSpan
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.pfejin.escapegameiot.R

class MessageListAdapter() : RecyclerView.Adapter<MessageListAdapter.MessageViewHolder>() {

    public var messageList: List<Message> = emptyList()

    class MessageViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        fun bind(message: Message) {
            itemView.apply {
                val textView = findViewById<TextView>(R.id.message)
                textView.text = message.text
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MessageViewHolder {
        return when (viewType) {
            0 -> {
                val itemView = LayoutInflater.from(parent.context).inflate(R.layout.player_message, parent, false)
                MessageViewHolder(itemView)
            }
            else -> {
                val itemView = LayoutInflater.from(parent.context).inflate(R.layout.gm_message, parent, false)
                MessageViewHolder(itemView)
            }
        }
    }

    override fun onBindViewHolder(holder: MessageViewHolder, position: Int) {
        holder.bind(messageList[position])
    }

    override fun getItemCount(): Int {
        return messageList.size;
    }

    override fun getItemViewType(position: Int): Int {
        return messageList[position].author.ordinal
    }

}