package com.pfejin.escapegameiot.messageList

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.view.animation.LayoutAnimationController
import android.widget.ImageView
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.pfejin.escapegameiot.R


class MessageListFragment : Fragment() {

    private val messageListViewModel: MessageListViewModel by viewModels()

    private val adapter = MessageListAdapter()

    private lateinit var recyclerView: RecyclerView

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_message_list, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        recyclerView = view.findViewById(R.id.recycler_view)

        recyclerView.layoutManager = LinearLayoutManager(activity)
        recyclerView.adapter = adapter

        messageListViewModel.messagesList.observe(viewLifecycleOwner, Observer {
            val position = it.size - 1

            recyclerView.layoutAnimationListener = object : Animation.AnimationListener {
                override fun onAnimationStart(animation: Animation?) {
                    for (i in 0 until position) {
                        recyclerView.layoutManager?.findViewByPosition(i)?.clearAnimation()
                    }
                }

                override fun onAnimationEnd(animation: Animation?) {}
                override fun onAnimationRepeat(animation: Animation?) {}
            }

            adapter.messageList = it
            adapter.notifyItemInserted(position)
            recyclerView.scheduleLayoutAnimation();
            recyclerView.layoutManager?.scrollToPosition(position)
        })

        val nextEnigmaButton = view.findViewById<FloatingActionButton>(R.id.next_enigma)
        nextEnigmaButton.setOnClickListener {
            messageListViewModel.sendFinished()
            messageListViewModel.receiveFinished()
        }

        val hintButton = view.findViewById<FloatingActionButton>(R.id.hint)
        hintButton.setOnClickListener {
            messageListViewModel.sendQuestion()
            messageListViewModel.receiveHint()
        }

        val previousEnigmaButton = view.findViewById<FloatingActionButton>(R.id.previous_enigma)
        previousEnigmaButton.setOnClickListener {
            messageListViewModel.sendUnfinished()
            messageListViewModel.receiveHint()
        }

        messageListViewModel.startGM()
    }
}